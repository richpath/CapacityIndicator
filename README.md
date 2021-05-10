# Capacity Indicator
<p>Code and documentation for Patient Capacity Level Indicator devices, currently under development in collaboration with Denver Health.</p>
<p>The project presently uses a Raspberry Pi Zero W V. 1.1 and a 32GB microSDHC card.</br>
OS = Raspberry Pi Lite, kernel version 5.10; see <strong>https://www.raspberrypi.org/software/operating-systems/</strong></p>
<p><strong>File details:</strong></p>
<p><strong>email_eval_commented.py</strong> - The current Python program used for evaluating alert status emails and updating the LEDs. Includes detailed comments within code describing operations.</p>
<p><strong>prototype_wiring_diagram.jpg</strong> - Wiring diagram of the project's prototype, created with Fritzing and Adobe Illustrator.</p>
<p><strong>capacity_indicator_levels_demo.mp4</strong> - A short video that shows the appearance of each alert level on the display.</p>
<p><strong>illuminated_capacity_level_indicator_prototype.jpg</strong> - Image of the display showing a red capacity alert level.</p>
<p><strong>Capacity indicator prototype materials list.pdf</strong> - A list of materials and costs for the construction of the indicator prototype.</p>
<p><strong>crontab</strong> - This text file is used by the Pi OS cron function to automate commands to be executed at recurring intervals. In this case, it runs two programs every minute to check wireless connection (and restart it if needed) and to check for new capacity level alert emails and update the LEDs of the display. Comments are included in the code for further details. For more information on using cron and crontab on a Pi or in Linux, see https://www.raspberrypi.org/documentation/linux/usage/cron.md</p>
