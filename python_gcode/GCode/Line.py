from .GCode import GCode
import numpy as np

a = 10  # [mm]. Shorest leg of the triangle will be 10 mm, 1 cm, 0.01 m long.
default_feed = 300  # mm/n
default_power = 150  # [dimensionless]


"""
# Default Line

Sane default for the ```draw_line``` command. Designed so that ```draw_line()``` does something that is easly measureable.

Draw a 30-60-90 triangle.

From: https://www.dummies.com/education/math/calculus/how-to-work-with-30-60-90-degree-triangles.

If you look at the 30:60:90-degree triangle in radians, it translates to the following:

$$\frac{\pi}{6}:\frac{\pi}{3}:\frac{\pi}{2}$$

In any 30-60-90 triangle, you see the following:

- The shortest leg is across from the 30-degree angle.

- The length of the hypotenuse is always two times the length of the shortest leg.

- You can find the long leg by multiplying the short leg by the square root of 3.

If you know one side of a 30-60-90 triangle, you can find the other two by using shortcuts. Here are the three situations you come across when doing these calculations:

- **Type 1**: You know the short leg (the side across from the 30-degree angle). Double its length to find the hypotenuse. You can multiply the short side by the square root of 3 to find the long leg.

- **Type 2**: You know the hypotenuse. Divide the hypotenuse by 2 to find the short side. Multiply this answer by the square root of 3 to find the long leg.

- **Type 3**: You know the long leg (the side across from the 60-degree angle). Divide this side by the square root of 3 to find the short side. Double that figure to find the hypotenuse.

Let:

- a: Shortest Side. Opposite 30$^o$ ($\frac{\pi}{6}$)
"""
default_points = np.array(
    [
        [0, 0],  # Start at origin.
        [a * np.sqrt(3), 0],  # Draw long side along X axis.
        [a * np.sqrt(3), a],  # Draw the short side parallel to Y axis.
        [0, 0],  # Return to origin. Draw hypotenuse.
    ]
)


class Line(GCode):
    def __init__(
        self,
        points=default_points,
        feed=default_feed,
        power=default_power,
        dynamic_power=True,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.points = points
        self.feed = feed
        self.power = power
        self.dynamic_power = dynamic_power

    def generate_gcode(self):
        self.buffer = list()
        self.G0(F=60)  # 60 mm / min = 1 mm / sec
        self.G1(F=60)  # 60 mm / min = 1 mm / sec
        self.M3(
            S=1
        )  # Set laser power so that movement can be seen, but does nothing.
        self.G28()  # "Home"
        self.G21()  # Metric Units
        self.G90()  # Absolute positioning.
        self.G92(
            X=0, Y=0, Z=0
        )  # The cliche, I forgot why I added it. It works. Don't touch it.

        self.G0(X=self.points[0, 0], Y=self.points[0, 1])

        if self.dynamic_power:
            self.M4(S=self.power)
        else:
            self.M4(S=self.power)

        for row_idx in range(1, self.points.shape[0]):
            self.G1(
                X=self.points[row_idx, 0],
                Y=self.points[row_idx, 1],
                F=self.feed,
            )
        self.M5()