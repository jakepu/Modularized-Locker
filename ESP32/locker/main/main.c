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
#define GPIO_LOCK_EN    (12)        // dev kit pin
// #define GPIO_LOCK_EN    (41)        // actual pin on PCB
#define BAUD_RATE       (115200)
#defind MSG_LEN         (6)
#define LOCK_OPEN_TICKS (1500 / portTICK_RATE_MS)
#define UART_BUF_SIZE (127)
#define UART_USED               UART_NUM_1
// Read packet timeout
#define PACKET_READ_TICS        (100 / portTICK_RATE_MS)
#define UART_TASK_STACK_SIZE    (2048)
#define UART_TASK_PRIO          (10)                        // max at 24
#define ECHO_UART_PORT          (CONFIG_ECHO_UART_PORT_NUM)


static void uart_send(const int port, const char* str, uint8_t length) 
{    
    if (uart_write_bytes(port, str, length) != length) {
        // ESP_LOGE(TAG, "Send data critical failure.");
        // add your code to handle sending failure here
        printf("uart_send failed");
        abort();
    }
}

// /*
//  * Define UART interrupt subroutine to handle parity error
//  */
// static void uart_intr_parity_err_handle(void *arg){
//     uart_flush(UART_USED);
//     uart_clear_intr_status(UART_USED, UART_PARITY_ERR_INT_CLR);
// }

static void monitor_uart_task(void *arg)
{
    uart_config_t uart_config = {
        .baud_rate = BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_EVEN,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_MODE_UART,        // no need for RS485 mode since it just uses RX
        .rx_flow_ctrl_thresh = 122,
        // .source_clk = UART_SCLK_APB,
    };

    // Configure UART parameters
    ESP_ERROR_CHECK(uart_param_config(UART_USED, &uart_config));

    // Set UART pins(TX: IO17 (UART1 default), RX: IO18 (UART1 default), RTS: IO19, CTS: IO20)
    ESP_ERROR_CHECK(uart_set_pin(UART_USED, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));

    ESP_ERROR_CHECK(uart_driver_install(UART_USED, UART_BUF_SIZE, UART_BUF_SIZE, 0, NULL, 0));

    // Allocate buffers for UART
    uint8_t data[UART_BUF_SIZE] = {0};

    // using WIFI MAC address to create unique ID for each chip
    char baseMac[MSG_LEN] = {0};
    esp_read_mac(baseMac, ESP_MAC_WIFI_STA);

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
    gpio_config(&io_conf);
    ESP_ERROR_CHECK(gpio_set_level(GPIO_LOCK_EN, 0));
    
    while(1) {
        // check every 1s
        vTaskDelay(1000 / portTICK_RATE_MS);
        //Read data from UART
        size_t buffered_len = 0;
        uart_get_buffered_data_len(UART_USED, buffered_len);
        // ignore corrupt msg and empty buffer
        if (buffered_len == 0) {continue;} 
        if (buffered_len != MSG_LEN) {
            uart_flush(UART_USED);
            continue;
        }
        int len = uart_read_bytes(UART_USED, &data, UART_BUF_SIZE, PACKET_READ_TICS);
        int addressed_flag = 1;
        for (int i = 0; i < MSG_LEN; i++) {
            if (baseMac[i] != data[i]) {addressed_flag = 0;}
        }
        if (addressed_flag){
            // open the lock for 1.5s
            ESP_ERROR_CHECK(gpio_set_level(GPIO_LOCK_EN, 1));
            vTaskDelay(LOCK_OPEN_TICKS);
            ESP_ERROR_CHECK(gpio_set_level(GPIO_LOCK_EN, 0));
        }
    }
    vTaskDelete(NULL);
}

void app_main(void)
{
    TaskHandle_t uart_task_handle;
    xTaskCreate(monitor_uart_task, "monitor_uart_task", UART_TASK_STACK_SIZE, NULL, UART_TASK_PRIO, &uart_task_handle);
}
