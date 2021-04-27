# Modularized Smart Locker

This is the GitHub site for Team 61 in 2021 Fall ECE 445 Senior Design Lab. We designed a modularized smart locker solution to improve 



# Contributor
- Jack Davis
- Jake Pu
- Josh Nolan

# To Do 
There are few things that we have not done but we think could be done to push this idea to perfection.
1. **Huge and Important Change**: Change UART on RS485 to I2C Differential. I2C is already a very mature protocol that supports multi-master multi-slave mode and handles collision elegantly. Putting I2C on differential signal can deliver signal to at least 3 meters far (much farther given our low bandwidth requirement & matching clock frequency. In this way, we can easily check the delivery status of the messages on the bus. The I2C addressing is also very helpful so that we do not have to do it ourselves.
