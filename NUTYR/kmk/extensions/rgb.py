from adafruit_pixelbuf import PixelBuf

from kmk.extensions import Extension
from kmk.scheduler import create_task
from kmk.utils import Debug, clamp

debug = Debug(__name__)

rgb_config = {}

def hsv_to_rgb(hue, sat, val):
    '''
    Converts HSV values, and returns a tuple of RGB values
    :param hue:
    :param sat:
    :param val:
    :return: (r, g, b)
    '''
    if sat == 0:
        return (val, val, val)

    hue = 6 * (hue & 0xFF)
    frac = hue & 0xFF
    sxt = hue >> 8

    base = (0xFF - sat) * val
    color = (val * sat * frac) >> 8
    val <<= 8

    if sxt == 0:
        r = val
        g = base + color
        b = base
    elif sxt == 1:
        r = val - color
        g = val
        b = base
    elif sxt == 2:
        r = base
        g = val
        b = base + color
    elif sxt == 3:
        r = base
        g = val - color
        b = val
    elif sxt == 4:
        r = base + color
        g = base
        b = val
    elif sxt == 5:
        r = val
        g = base
        b = val - color

    return (r >> 8), (g >> 8), (b >> 8)

def hsv_to_rgbw(hue, sat, val):
    '''
    Converts HSV values, and returns a tuple of RGBW values
    :param hue:
    :param sat:
    :param val:
    :return: (r, g, b, w)
    '''
    rgb = hsv_to_rgb(hue, sat, val)
    return rgb[0], rgb[1], rgb[2], min(rgb)



class RGB(Extension):
    pos = 0

    def __init__(
        self,
        pixel_pin,
        num_pixels=6,
        rgb_order=(1, 0, 2),  # GRB WS2812
        val_limit=255,
        hue_default=0,
        sat_default=255,
        val_default=255,
        hue_step=4,
        sat_step=13,
        val_step=13,
        animation_speed=1,
        breathe_center=1,  # 1.0-2.7
        knight_effect_length=3,
        effect_init=False,
        reverse_animation=False,
        user_animation=None,
        pixels=None,
        refresh_rate=20,
    ):
        self.pixel_pin = pixel_pin
        self.num_pixels = num_pixels
        self.rgb_order = rgb_order
        self.hue_step = hue_step
        self.sat_step = sat_step
        self.val_step = val_step
        self.hue = hue_default
        self.hue_default = hue_default
        self.sat = sat_default
        self.sat_default = sat_default
        self.val = val_default
        self.val_default = val_default
        self.breathe_center = breathe_center
        self.knight_effect_length = knight_effect_length
        self.val_limit = val_limit
        self.animation_speed = animation_speed
        self.effect_init = effect_init
        self.reverse_animation = reverse_animation
        self.user_animation = user_animation
        self.pixels = pixels
        self.refresh_rate = refresh_rate

        self.rgbw = bool(len(rgb_order) == 4)

        self._substep = 0



    def during_bootup(self, sandbox):
        if self.pixels is None:
            import neopixel

            self.pixels = neopixel.NeoPixel(
                self.pixel_pin,
                self.num_pixels,
                pixel_order=self.rgb_order,
            )
        print(pixels)
        # PixelBuffer are already iterable, can't do the usual `try: iter(...)`
        if issubclass(self.pixels.__class__, PixelBuf):
            self.pixels = (self.pixels,)

        # Turn off auto_write on the backend. We handle the propagation of auto_write
        # behaviour.
        for pixel in self.pixels:
            pixel.auto_write = False

        if self.num_pixels == 0:
            for pixels in self.pixels:
                self.num_pixels += len(pixels)

        if debug.enabled:
            for n, pixels in enumerate(self.pixels):
                debug(f'pixels[{n}] = {pixels.__class__}[{len(pixels)}]')

        self._task = create_task(self.animate, period_ms=(1000 // self.refresh_rate))

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        pass

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        self._do_update()

    def deinit(self, sandbox):
        for pixel in self.pixels:
            pixel.deinit()

    def set_rgb(self, rgb, index):
        '''
        Takes an RGB or RGBW and displays it on a single LED/Neopixel
        :param rgb: RGB or RGBW
        :param index: Index of LED/Pixel
        '''
        if 0 <= index <= self.num_pixels - 1:
            for pixels in self.pixels:
                if index <= (len(pixels) - 1):
                    pixels[index] = rgb
                    break
                index -= len(pixels)

    def set_rgb_fill(self, rgb):
        '''
        Takes an RGB or RGBW and displays it on all LEDs/Neopixels
        :param rgb: RGB or RGBW
        '''
        for pixels in self.pixels:
            pixels.fill(rgb)



    def show(self):
        '''
        Turns on all LEDs/Neopixels without changing stored values
        '''
        for pixels in self.pixels:
            pixels.show()

    def animate(self):
        return
        '''
        Activates a "step" in the animation based on the active mode
        :return: Returns the new state in animation
        '''
       


        if not self.enable:
            return

    

        self.effect_static()

        self.show()

    def _animation_step(self):
        self._substep += self.animation_speed / 4
        self._step = int(self._substep)
        self._substep -= self._step

    def _init_effect(self):
        self.pos = 0
        self.reverse_animation = False
        self.effect_init = False

    def _check_update(self):
        return False

    def effect_static(self):
        self.set_hsv_fill(self.hue, self.sat, self.val)

    def _rgb_reset(self, *args, **kwargs):
        self.hue = self.hue_default
        self.sat = self.sat_default
        self.val = self.val_default
        self._do_update()

    
    def set_hsv_fill(self, hue, sat, val):
        '''
        Takes HSV values and displays it on all LEDs/Neopixels
        :param hue:
        :param sat:
        :param val:
        '''

        val = clamp(val, 0, self.val_limit)

        if self.rgbw:
            self.set_rgb_fill(hsv_to_rgbw(hue, sat, val))
        else:
            self.set_rgb_fill(hsv_to_rgb(hue, sat, val))

