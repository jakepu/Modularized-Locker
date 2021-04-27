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
#define GPIO_LOCK_EN    (23)        // dev kit pin
// #define GPIO_LOCK_EN    (41)        // actual pin on PCB
#define BAUD_RATE       (115200)
#define MSG_LEN         (6)
#define LOCK_OPEN_TICKS (1500 / portTICK_RATE_MS)
#define UART_BUF_SIZE (256)
#define UART_USED               UART_NUM_1
// Read packet timeout
#define PACKET_READ_TICS        (100 / portTICK_RATE_MS)
#define UART_TASK_STACK_SIZE    (2048)
#define UART_TASK_PRIO          (10)                        // max at 24
#define EVENT_QUEUE_SIZE        (20)
#define RTS_PIN               (21) 

static void uart_send(const int port, const uint8_t* str, uint8_t length) 
{   
    if (uart_write_bytes(port, (const char *)str, length) != length) {
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
    // Set UART pins(TX: IO17 (UART1 default), RX: IO18 (UART1 default), RTS: IO33, CTS: IO34)
    ESP_ERROR_CHECK(uart_set_pin(UART_USED, 17, 18, RTS_PIN, 34));
    ESP_ERROR_CHECK(uart_driver_install(UART_USED, UART_BUF_SIZE, UART_BUF_SIZE, 0, NULL, 0));
    ESP_ERROR_CHECK(uart_set_mode(UART_USED, UART_MODE_RS485_HALF_DUPLEX));
    // Allocate buffers for UART
    uint8_t data[UART_BUF_SIZE] = {0};

    // using WIFI MAC address to create unique ID for each chip
    uint8_t baseMac[MSG_LEN] = {156, 156, 31, 199, 191, 120};

    
    uart_event_t event;
    while(1) {
        vTaskDelay(4000 / portTICK_RATE_MS);
        //Read data from UART
        size_t buffered_len = 0;
        uart_send(UART_USED, baseMac, 6);
        printf("Sent to mac address is: %u, %u, %u, %u, %u, %u\n", baseMac[0], baseMac[1], baseMac[2], baseMac[3], baseMac[4], baseMac[5]);
    }
    vTaskDelete(NULL);
}

void app_main(void)
{
    TaskHandle_t uart_task_handle;
    xTaskCreate(monitor_uart_task, "monitor_uart_task", UART_TASK_STACK_SIZE, NULL, UART_TASK_PRIO, &uart_task_handle);
}
