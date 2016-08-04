## Install Raspbian Jessie

Download a copy of the img [here](https://www.raspberrypi.org/downloads/raspbian/)

Follow instructions for your OS:

[Linux](#linux)

[Mac OS](#mac)

[Windows](#windows)


#### <a name="linux"></a> Linux

<ul>
<li>
<p>Run <code>df -h</code> to see what devices are currently mounted.</p>
</li>
<li>
<p>If your computer has a slot for SD cards, insert the card. If not, insert the card into an SD card reader, then connect the reader to your computer.</p>
</li>
<li>
<p>Run <code>df -h</code> again. The new device that has appeared is your SD card. The left column gives the device name of your SD card; it will be listed as something like <code>/dev/mmcblk0p1</code> or <code>/dev/sdd1</code>. The last part (<code>p1</code> or <code>1</code> respectively) is the partition number but you want to write to the whole SD card, not just one partition. You therefore need to remove that part from the name, getting, for example, <code>/dev/mmcblk0</code> or <code>/dev/sdd</code> as the device name for the whole SD card. Note that the SD card can show up more than once in the output of <code>df</code>; it will do this if you have previously written a Raspberry Pi image to this SD card, because the Raspberry Pi SD images have more than one partition.</p>
</li>
<li>
<p>Now that you've noted what the device name is, you need to unmount it so that files can't be read or written to the SD card while you are copying over the SD image.</p>
</li>
<li>
<p>Run <code>umount /dev/sdd1</code>, replacing <code>sdd1</code> with whatever your SD card's device name is (including the partition number).</p>
</li>
<li>
<p>If your SD card shows up more than once in the output of <code>df</code> due to having multiple partitions on the SD card, you should unmount all of these partitions.</p>
</li>
<li>
<p>In the terminal, write the image to the card with the command below, making sure you replace the input file <code>if=</code> argument with the path to your <code>.img</code> file, and the <code>/dev/sdd</code> in the output file <code>of=</code> argument with the right device name. This is very important, as you will lose all data on the hard drive if you provide the wrong device name. Make sure the device name is the name of the whole SD card as described above, not just a partition of it; for example, <code>sdd</code>, not <code>sdds1</code> or <code>sddp1</code>, and <code>mmcblk0</code>, not <code>mmcblk0p1</code>.</p>
<pre><code class="language-bash">dd bs=4M if=2016-05-27-raspbian-jessie.img of=/dev/sdd</code></pre>
</li>
<li>
<p>Please note that block size set to <code>4M</code> will work most of the time; if not, please try <code>1M</code>, although this will take considerably longer.</p>
</li>
<li>
<p>Also note that if you are not logged in as root you will need to prefix this with <code>sudo</code>.</p>
</li>
<li>
<p>The <code>dd</code> command does not give any information of its progress and so may appear to have frozen; it could take more than five minutes to finish writing to the card. If your card reader has an LED it may blink during the write process. To see the progress of the copy operation you can run <code>pkill -USR1 -n -x dd</code> in another terminal, prefixed with <code>sudo</code> if you are not logged in as root. The progress will be displayed in the original window and not the window with the <code>pkill</code> command; it may not display immediately, due to buffering.</p>
</li>
<li>
<p>Instead of <code>dd</code> you can use <code>dcfldd</code>; it will give a progress report about how much has been written.</p>
</li>
<li>
<p>You can check what's written to the SD card by <code>dd</code>-ing from the card back to another image on your hard disk, truncating the new image to the same size as the original, and then running <code>diff</code> (or <code>md5sum</code>) on those two images.</p>
</li>
<li>
<p>The SD card might be bigger than the original image, and <code>dd</code> will make a copy of the whole card. We must therefore truncate the new image to the size of the original image. Make sure you replace the input file <code>if=</code> argument with the right device name. <code>diff</code> should report that the files are identical.</p>
<pre><code class="language-bash">dd bs=4M if=/dev/sdd of=from-sd-card.img
truncate --reference 2016-05-27-raspbian-jessie.img from-sd-card.img
diff -s from-sd-card.img 2016-05-27-raspbian-jessie.img</code></pre>
</li>
<li>
<p>Run <code>sync</code>; this will ensure the write cache is flushed and that it is safe to unmount your SD card.</p>
</li>
<li>Remove the SD card from the card reader.</li>
</ul>
<hr />

#### mac OS <a name="mac"></a>

<p>Run <code>diskutil list</code></p>
</li>
<li>Identify the disk (not partition) of your SD card e.g. <code>disk4</code>, not <code>disk4s1</code>.</li>
<li>
<p>Unmount your SD card by using the disk identifier, to prepare for copying data to it:</p>
<p><code>diskutil unmountDisk /dev/disk&lt;disk# from diskutil&gt;</code></p>
<p>where <code>disk</code> is your BSD name e.g. <code>diskutil unmountDisk /dev/disk4</code></p>
</li>
<li>
<p>Copy the data to your SD card:</p>
<p><code>sudo dd bs=1m if=image.img of=/dev/rdisk&lt;disk# from diskutil&gt;</code></p>
<p>where <code>disk</code> is your BSD name e.g. <code>sudo dd bs=1m if=2016-05-27-raspbian-jessie.img of=/dev/rdisk4</code></p>
<ul>
<li>
<p>This may result in a <code>dd: invalid number '1m'</code> error if you have GNU
coreutils installed. In that case, you need to use a block size of <code>1M</code> in the <code>bs=</code> section, as follows:</p>
<p><code>sudo dd bs=1M if=image.img of=/dev/rdisk&lt;disk# from diskutil&gt;</code></p>
</li>
</ul>
<p>This will take a few minutes, depending on the image file size. You can check the progress by sending a <code>SIGINFO</code> signal (press <code>Ctrl+T</code>).</p>
<ul>
<li>
<p>If this command still fails, try using <code>disk</code> instead of <code>rdisk</code>, for example:</p>
<pre><code>sudo dd bs=1m if=2016-05-27-raspbian-jessie.img of=/dev/disk4</code></pre>
<p>or</p>
<pre><code>sudo dd bs=1M if=2016-05-27-raspbian-jessie.img of=/dev/disk4</code></pre>
</li>
</ul>
</li>
</ul>
<h2>Alternative method</h2>
<p><strong>Note: Some users have reported issues with using this method to create SD cards.</strong></p>
<p>These commands and actions need to be performed from an account that has administrator privileges.</p>
<ul>
<li>From the terminal run <code>df -h</code>.</li>
<li>Connect the SD card reader with the SD card inside.</li>
<li>Run <code>df -h</code> again and look for the new device that wasn't listed last time. Record the device name of the filesystem's partition, for example <code>/dev/disk3s1</code>.</li>
<li>
<p>Unmount the partition so that you will be allowed to overwrite the disk:</p>
<pre><code>sudo diskutil unmount /dev/disk3s1</code></pre>
<p>Alternatively, open Disk Utility and unmount the partition of the SD card; do not eject it, or you will have to reconnect it.</p>
</li>
<li>Using the device name of the partition, work out the <em>raw device name</em> for the entire disk by omitting the final <code>s1</code> and replacing <code>disk</code> with <code>rdisk</code> This is very important, as you will lose all data on the hard drive if you provide the wrong device name. Make sure the device name is the name of the whole SD card as described above, not just a partition of it - for example, <code>rdisk3</code>, not <code>rdisk3s1</code>. Similarly, you might have another SD drive name/number like <code>rdisk2</code> or <code>rdisk4</code>; you can check again by using the <code>df -h</code> command both before and after you insert your SD card reader into your Mac. For example, <code>/dev/disk3s1</code> becomes <code>/dev/rdisk3</code>.</li>
<li>
<p>In the terminal, write the image to the card with this command, using the raw device name from above. Read the above step carefully to be sure you use the correct <code>rdisk</code> number here:</p>
<pre><code>sudo dd bs=1m if=2016-05-27-raspbian-jessie.img of=/dev/rdisk3</code></pre>
<p>If the above command reports the error <code>dd: bs: illegal numeric value</code>, please change the block size <code>bs=1m</code> to <code>bs=1M</code>.</p>
<p>If the above command reports the error <code>dd: /dev/rdisk3: Permission denied</code>, it means the partition table of the SD card is being protected against being overwritten by Mac OS. Erase the SD card's partition table using this command:</p>
<pre><code>sudo diskutil partitionDisk /dev/disk3 1 MBR "Free Space" "%noformat%" 100%</code></pre>
<p>That command will also set the permissions on the device to allow writing. Now try the <code>dd</code> command again.</p>
<p>Note that <code>dd</code> will not provide any on-screen information until there is an error or it is finished; when complete, information will be shown and the disk will re-mount. If you wish to view the progress, you can use <code>Ctrl-T</code>; this generates SIGINFO, the status argument of your terminal, and will display information on the process.</p>
</li>
<li>
<p>After the <code>dd</code> command finishes, eject the card:</p>
<pre><code>sudo diskutil eject /dev/rdisk3</code></pre>
<p>Alternatively, open Disk Utility and use this to eject the SD card.</p>
</li>
</ul>

#### <a name="windows"></a> Windows

<ul>
<li>Insert the SD card into your SD card reader and check which drive letter was assigned. You can easily see the drive letter, such as <code>G:</code>, by looking in the left column of Windows Explorer. You can use the SD card slot if you have one, or a cheap SD adapter in a USB port.</li>
<li>Download the Win32DiskImager utility from the <a href="http://sourceforge.net/projects/win32diskimager/">Sourceforge Project page</a> as a zip file; you can run this from a USB drive.</li>
<li>Extract the executable from the zip file and run the <code>Win32DiskImager</code> utility; you may need to run this as administrator. Right-click on the file, and select <strong>Run as administrator</strong>.</li>
<li>Select the image file you extracted earlier.</li>
<li>Select the drive letter of the SD card in the device box. Be careful to select the correct drive; if you get the wrong one you can destroy the data on your computer's hard disk! If you are using an SD card slot in your computer and can't see the drive in the Win32DiskImager window, try using an external SD adapter.</li>
<li>Click <code>Write</code> and wait for the write to complete.</li>
<li>Exit the imager and eject the SD card.</li>
</ul>
