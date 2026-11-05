# Runbook: DNS actions for adding a new device to the Home Lab

Use this when adding a new devices to the Home Lab. This is done for devices with "significant" names. Names are "significant" if the devices are referred to or accessed over the LAN by other devices.

## 1. Triage: Is this name "significant"?

| Class | Examples | Response |
|---|---|---|
| **Not Signficant** | "Toaster" - This device uses the LAN to update software, but nobody cares. It's a *toaster*.
| **Signficant** | "SumDataMuncher" - This server would be used presumably for munching data by other devices. | Walk through the following process. |

If unsure, treat it as one class higher, then leave it. It's a manual DNS entry, and we are more likely to run out of numbers than names.

## 2. The sequence

1. **Notice.** The WiFi Mesh notifies of a new device logging in. Access that device within the LAN admin on the cell phone and note the default name offered or choose a new simple name relevant to the function.
2. **Edit Appearance.** In this same admin window, choose how the device appears which also groups it by device type. Generally, this will either be "Network Equipment" for services or "Game Console" for game servers, but "close enough" will do. You want to visually note what kind of device this is in a list in addition to the name.
3. **Select DNS #** Bring up the DNS admin, under the "Settings" look for the "Local DNS Settings", then find the next available IP address in the series. It will be a number below 132. "Stale" addresses may remain stale, numbers are cheap.
4. **Set up reservation in DHCP** Back on the mesh admin app, select the new devices, edit the IP to match the number selected in your DNS admin, then save.
5. **Verify.** Reboot the device to load the new DHCP provided IP, then use `ping` on the device name, then log into the device by name to verify the newly named devices works as expected.
7. **Record.** The named device information is stored in the admin of the Mesh Admin and within the DNS Admin.

## 3. Future Plans

In the future, an easier boarding process should be created for the information to be managed by a single devices. This must wait until the Home Lab has a wealth of priority issues to resolve.
