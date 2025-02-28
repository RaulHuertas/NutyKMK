from supervisor import ticks_ms

import displayio
from adafruit_display_text import label

from kmk.extensions import Extension
from kmk.kmktime import PeriodicTimer, ticks_diff
from kmk.utils import clamp
import terminalio
class DisplayBase:
    def __init__(self):
        raise NotImplementedError

    def during_bootup(self, width, height, rotation):
        raise NotImplementedError

    def deinit(self):
        raise NotImplementedError

    def sleep(self):
        self.display.sleep()

    def wake(self):
        self.display.wake()

    @property
    def brightness(self):
        return self.display.brightness

    @brightness.setter
    def brightness(self, new_brightness):
        self.display.brightness = new_brightness

    # display.show() is deprecated, so use root_group instead
    @property
    def root_group(self):
        return self.display.root_group

    @root_group.setter
    def root_group(self, group):
        self.display.root_group = group


class Display(Extension):
    def __init__(
        self,
        display=None,
        entries=[],
        brightness=0.8,
        brightness_step=0.1,
        dim_time=20,
        dim_target=0.1,
        off_time=60,
        powersave_dim_time=10,
        powersave_dim_target=0.1,
        powersave_off_time=30,
    ):
        self.display = display
        self.entries = entries
        self.width = display.width
        self.height = display.height
        self.rotation = display.rotation
        self.prev_layer = None
        self.brightness = brightness
        self.brightness_step = brightness_step
        self.timer_start = ticks_ms()
        self.dim_time_ms = dim_time * 1000
        self.dim_target = dim_target
        self.off_time_ms = off_time * 1000
        self.powersavedim_time_ms = powersave_dim_time * 1000
        self.powersave_dim_target = powersave_dim_target
        self.powersave_off_time_ms = powersave_off_time * 1000
        self.powersave = False
        self.dim_period = PeriodicTimer(50)
        self.split_side = None
        self.showBoot = True
        #layer1 = bitmap = displayio.OnDiskBitmap("/layer1.bmp")
        #self.layer1 = displayio.TileGrid(layer1, pixel_shader=layer1.pixel_shader,x=0,y=0)
        
        
        #layer2 = bitmap = displayio.OnDiskBitmap("/layer2.bmp")
        #self.layer2 = displayio.TileGrid(layer2, pixel_shader=layer2.pixel_shader,x=0,y=0)

        #make_key(names=('DIS_BRI',), on_press=self.display_brightness_increase)
        #make_key(names=('DIS_BRD',), on_press=self.display_brightness_decrease)

    def render(self, layer):
        if self.showBoot:
            self.showBoot = False
            splash = displayio.Group()
            splash.append(
                label.Label(
                    terminalio.FONT,
                    text="Activando escudos AT",
                    color=0xFFFFFF,
                    x=0,
                    y=4,
                )
            )
            self.display.root_group = splash
            import time
            time.sleep(1)
            return
        splash = displayio.Group()

            #if isinstance(entry, TextEntry):
        splash.append(
            label.Label(
                terminalio.FONT,
                text="Capa: "+str(layer+1),
                color=0xFFFFFF,
                x=0,
                y=4,                
            )
        )
            #   pass
            #elif isinstance(entry, ImageEntry):
                #splash.append(
                #    displayio.TileGrid(
                #        entry.image,
                #        pixel_shader=entry.image.pixel_shader,
                #        x=entry.x,
                #        y=entry.y,
                #    )
                #)
                #pass
        self.display.root_group = splash

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):
        self.display.during_bootup(self.width, self.height,self.rotation)
        self.display.brightness = self.brightness

    def before_matrix_scan(self, sandbox):
        if self.dim_period.tick():
            self.dim()
        if sandbox.active_layers[0] != self.prev_layer:
            print("layer change detected")
            self.prev_layer = sandbox.active_layers[0]
            self.render(sandbox.active_layers[0])

    def after_matrix_scan(self, sandbox):
        if sandbox.matrix_update or sandbox.secondary_matrix_update:
            self.timer_start = ticks_ms()

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        self.powersave = True

    def on_powersave_disable(self, sandbox):
        self.powersave = False

    def deinit(self, sandbox):
        displayio.release_displays()
        self.display.deinit()

    def display_brightness_increase(self, *args):
        self.display.brightness = clamp(
            self.display.brightness + self.brightness_step, 0, 1
        )
        self.brightness = self.display.brightness  # Save current brightness

    def display_brightness_decrease(self, *args):
        self.display.brightness = clamp(
            self.display.brightness - self.brightness_step, 0, 1
        )
        self.brightness = self.display.brightness  # Save current brightness

    def dim(self):
        if self.powersave:
            if (
                self.powersave_off_time_ms
                and ticks_diff(ticks_ms(), self.timer_start)
                > self.powersave_off_time_ms
            ):
                self.display.sleep()

            elif (
                self.powersave_dim_time_ms
                and ticks_diff(ticks_ms(), self.timer_start)
                > self.powersave_dim_time_ms
            ):
                self.display.brightness = self.powersave_dim_target

            else:
                self.display.brightness = self.brightness
                self.display.wake()

        elif (
            self.off_time_ms
            and ticks_diff(ticks_ms(), self.timer_start) > self.off_time_ms
        ):
            self.display.sleep()

        elif (
            self.dim_time_ms
            and ticks_diff(ticks_ms(), self.timer_start) > self.dim_time_ms
        ):
            self.display.brightness = self.dim_target

        else:
            self.display.brightness = self.brightness
            self.display.wake()
