# Modularized Smart Locker

This is the GitHub site for Team 61 in 2021 Fall ECE 445 Senior Design Lab. We designed a modularized smart locker solution to lower the cost of making a smart locker like Amazon Hub Locker while providing a template full-stack solution to manufacturers to produce just 2 modules that can fulfill the various needs for a smart locker. By using 1 control modules and 1-127 locker modules (limited by RS485), we can provide a secure & smart locker solution to household customers and apartment owners.



# Contributor
- Jack Davis
- Jake Pu
- Josh Nolan

# How to run

## ESP32 on locker module
1. Install ESP-IDF following the [tutorial](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/).
2. Make sure you run `. $HOME/esp/esp-idf/export.sh`
3. Navigate to `./ESP32/deployment`
4. run `idf.py fullclean`
5. run `idf.py -p PORT flash`, on my Ubuntu laptop, the PORT is `/dev/ttyUSB0` with dev kit and `/dev/ttyACM0` with ESP32-S2-WROVER-I module.
6. **On the module, since RTS is not connected, we have to restart the module with the button on EN ourselves.**

## GUI on RPI

    cd ./RPI
    python3 gui.py


## Website
1. Navigate to the Website/server folder.
2. Run `node index.js` in the console.
3. Open a new console.
4. Type `npm start App.js`. It will launch a website in the web browser.

# To Do 
There are few things that we have not done but we think could be done to push this idea to perfection.
1. **Huge and Important Change**: Change UART on RS485 to I2C Differential. I2C is already a very mature protocol that supports multi-master multi-slave mode and handles collision elegantly. Putting I2C on differential signal can deliver signal to at least 3 meters far (much farther given our low bandwidth requirement & matching clock frequency. In this way, we can easily check the delivery status of the messages on the bus. The I2C addressing is also very helpful so that we do not have to do it ourselves. A suggested chip is the [NXP’s PCA9615 IC](https://www.nxp.com/docs/en/data-sheet/PCA9615.pdf).
