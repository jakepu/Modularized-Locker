#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "driver/uart.h"
#include "freertos/queue.h"
#include "esp_log.h"
#include "sdkconfig.h"
#include "driver/gpio.h"

// #define TAG "RS485_LOCKER_APP"
// #define GPIO_LOCK_EN    (23)        // dev kit pin
#define GPIO_LOCK_EN    (41)        // actual pin on PCB
#define BAUD_RATE       (115200)
#define MSG_LEN         (6)
#define LOCK_OPEN_TICKS (5000 / portTICK_RATE_MS)
#define UART_BUF_SIZE (256)
#define UART_USED               UART_NUM_1
// Read packet timeout
#define PACKET_READ_TICS        (100 / portTICK_RATE_MS)
#define UART_TASK_STACK_SIZE    (4096)
#define RESET_TASK_STACK_SIZE    (4096)
#define UART_TASK_PRIO          (10)                        // max at 24
#define RESET_TASK_PRIO          (10)                        // max at 24
#define EVENT_QUEUE_SIZE        (20)
// #define RESET_MODE_PIN               (22)                      // dev kit
#define RESET_MODE_PIN               (42)                       // actual pin
// since UART_MODE_RS485_HALF_DUPLEX is not controlling RTS well I will
// use a independent GPIO to work as RTS
#define RTS_PIN               (21) 

static QueueHandle_t uart1_queue;

static uint8_t baseMac[MSG_LEN] = {0};

static QueueHandle_t gpio_evt_queue = NULL;

static void uart_send(const int port, const uint8_t* str, uint8_t length) 
{   
    // since UART_MODE_RS485_HALF_DUPLEX is not controlling RTS, we are controlling RTS_PIN
    ESP_ERROR_CHECK(gpio_set_level(RTS_PIN,1));
    if (uart_write_bytes(port, (const char *)str, length) != length) {
        // ESP_LOGE(TAG, "Send data critical failure.");
        // add your code to handle sending failure here
        printf("uart_send failed");
        // abort();
    }
    // wait till all data is sent
    uart_wait_tx_done(UART_USED, 1000 / portTICK_RATE_MS);
    ESP_ERROR_CHECK(gpio_set_level(RTS_PIN, 0));
}

static void IRAM_ATTR reset_isr_handler(void* arg)
{
    uint8_t ack = 1;
    xQueueSendFromISR(gpio_evt_queue, &ack, NULL);
}


static void monitor_uart_task(void *arg)
{
    uart_config_t uart_config = {
        .baud_rate = BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_EVEN,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_MODE_UART,
        .rx_flow_ctrl_thresh = 122,
        .source_clk = UART_SCLK_APB,
    };

    // Configure UART parameters
    ESP_ERROR_CHECK(uart_param_config(UART_USED, &uart_config));

    // Set UART pins(TX: IO17 (UART1 default), RX: IO18 (UART1 default), RTS: IO21, CTS: IO33)
    ESP_ERROR_CHECK(uart_set_pin(UART_USED, 17, 18, 33, 34));

    
    ESP_ERROR_CHECK(uart_driver_install(UART_USED, UART_BUF_SIZE, UART_BUF_SIZE, EVENT_QUEUE_SIZE, &uart1_queue, 0));

    // Allocate buffers for UART
    uint8_t data[UART_BUF_SIZE] = {0};

    

    // setup GPIO to control NMOS
    gpio_config_t io_conf;
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = 1ULL << GPIO_LOCK_EN;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    ESP_ERROR_CHECK(gpio_config(&io_conf));
    ESP_ERROR_CHECK(gpio_set_level(GPIO_LOCK_EN, 0));
    
    uart_event_t event;
    while(1) {
        // check every 1s
        vTaskDelay(1000 / portTICK_RATE_MS);
        printf("The mac address is: %u, %u, %u, %u, %u, %u\n", baseMac[0], baseMac[1], baseMac[2], baseMac[3], baseMac[4], baseMac[5]);
        //Read data from UART
        size_t buffered_len = 0;
        uart_get_buffered_data_len(UART_USED, &buffered_len);
        printf("buffered_len: %u\n", buffered_len);
        // ignore corrupt msg and empty buffer
        if (buffered_len == 0) {continue;} 
        if (buffered_len != MSG_LEN) {
            uart_flush(UART_USED);
            xQueueReset(uart1_queue);
            continue;
        }
        uint8_t err = 0;
        while (uxQueueMessagesWaiting(uart1_queue) > 0) {
            xQueueReceive(uart1_queue, (void * )&event, 0);
            if (event.type == UART_PARITY_ERR || event.type == UART_FRAME_ERR) {
                err = 1;
                printf("event error\n");
                break;
            }
        }
        if (err) {
            uart_flush(UART_USED);
            xQueueReset(uart1_queue);
            continue;
        }
        int len = uart_read_bytes(UART_USED, data, UART_BUF_SIZE, PACKET_READ_TICS);
        int addressed_flag = 1;
        for (int i = 0; i < MSG_LEN; i++) {
            if (baseMac[i] != data[i]) {addressed_flag = 0;}
        }
        printf("Received mac address is: %u, %u, %u, %u, %u, %u\n", data[0], data[1], data[2], data[3], data[4], data[5]);
        if (addressed_flag){
            // open the lock for 1.5s
            printf("received msg to this device\n");
            ESP_ERROR_CHECK(gpio_set_level(GPIO_LOCK_EN, 1));
            vTaskDelay(LOCK_OPEN_TICKS);
            ESP_ERROR_CHECK(gpio_set_level(GPIO_LOCK_EN, 0));
        }
    }
    vTaskDelete(NULL);
}

void setup_reset_button() {
    gpio_config_t io_conf;
    io_conf.intr_type = GPIO_INTR_NEGEDGE;
    io_conf.pin_bit_mask = 1ULL << RESET_MODE_PIN;
    //set as input mode
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_up_en = 0;
    io_conf.pull_down_en = 0;
    ESP_ERROR_CHECK(gpio_config(&io_conf));
    ESP_ERROR_CHECK(gpio_install_isr_service(0));
    ESP_ERROR_CHECK(gpio_isr_handler_add(RESET_MODE_PIN, reset_isr_handler, NULL));
    gpio_evt_queue = xQueueCreate(1, sizeof(uint8_t));
}

void setup_rts_pin() {

    gpio_config_t io_conf;
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.pin_bit_mask = 1ULL << RTS_PIN;
    //set as input mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pull_up_en = 0;
    io_conf.pull_down_en = 0;
    ESP_ERROR_CHECK(gpio_config(&io_conf));
    ESP_ERROR_CHECK(gpio_set_level(RTS_PIN,0));
}

void reset_button_monitor_task() {
    uint8_t ack;
    while (true) {
        vTaskDelay(1000 / portTICK_RATE_MS);
        if (xQueueReceive(gpio_evt_queue, &ack, 0) == pdTRUE){
            uart_send(UART_USED, baseMac, MSG_LEN);
        }
    }
    vTaskDelete(NULL);
}

void app_main(void)
{
    // using WIFI MAC address to create unique ID for each chip
    esp_read_mac(baseMac, ESP_MAC_WIFI_STA);
    TaskHandle_t uart_task_handle;
    setup_reset_button();
    setup_rts_pin();
    xTaskCreate(monitor_uart_task, "monitor_uart_task", UART_TASK_STACK_SIZE, NULL, UART_TASK_PRIO, &uart_task_handle);
    xTaskCreate(reset_button_monitor_task, "reset_button_monitor_task", RESET_TASK_STACK_SIZE, NULL, RESET_TASK_PRIO, NULL);
}
