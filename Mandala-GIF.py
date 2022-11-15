#! python3
# Mandala-GIF.py - Mandala-GIF creates a GIF of a mandala-like design using Pillow.

import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import imageio as io
from pathlib import Path


class Mandala:
    """Overall class to create the mandala."""

    def __init__(self):
        """A method to control image settings, as well as run all class methods."""

        self.image_side = 1600
        self.frame_count = 30

        self.background_pattern_count = 8

        self.border_circle_divisor = 16
        self.circle_hue_count = 11
        self.circle_shrink = 1
        self.circle_line_distance = 5
        self.circle_line_width = 2
        self.circle_horizontal_stretch = 1
        self.circle_vertical_stretch = 1
        self.spoke_spin_clockwise = 0
        self.spoke_spin_counterclockwise = 0

        # Image effect settings
        self.posterize_bits = 8

        # Color variables
        self.grey_hue_count = 24
        self.green_hue_count = 24
        self.gold_hue_count = 24

        # Color lists
        self.background_colors = []
        self.circle_colors = []
        self.grey_tones = []
        self.green_tones = []
        self.gold_tones = []

        # GIF frame variables
        self.gif_frames = self.frame_count + 1
        self.current_frame = 1

        # Background variables
        self.background_pattern_size = int(self.image_side / self.background_pattern_count)
        self.background_hue_count = int(self.background_pattern_size / 2)

        # Circle variables
        self.image_center = int(self.image_side / 2)
        self.circle_size = self.image_side - (self.image_side / self.border_circle_divisor * 2)
        self.circle_radius = self.circle_size / 2
        self.circle_to_image_edge = self.image_side / self.border_circle_divisor
        self.circle_line_width_growth = 1
        self.circle_hue_count_growth = 1

        # Shape variables
        self.shape_width = self.circle_size / 3
        self.shape_ints = [self.shape_width / 2,
                           self.shape_width / 16,
                          (self.shape_width / 2) + (self.shape_width / 8),
                           self.shape_width / 6,
                           self.shape_width - (self.shape_width / 4)]

        self.platform_int = self.image_center - self.shape_ints[4] - (self.shape_ints[1] * 3.5) \
                            + ((self.shape_ints[4] - self.shape_ints[2]) / 3)

        # Spoke variables
        self.square_width = (self.shape_ints[4] + self.shape_ints[1]) * 2
        self.square_diagonal_squared = (self.square_width ** 2) + (self.square_width ** 2)
        self.square_diagonal = self.square_diagonal_squared ** 0.5

        # Inner square pattern variables.
        self.inner_square_pattern_stretch = 10
        self.inner_square_pattern_growth = 1

        # Border circle variables
        self.halo_spin_clockwise = 0
        self.halo_spin_counterclockwise = 0
        self.halo_spin_direction = 0

        # Create a list of settings.
        self.settings_list = [self.background_pattern_count,
                              self.border_circle_divisor,
                              self.circle_shrink,
                              self.circle_line_distance,
                              self.circle_horizontal_stretch,
                              self.circle_vertical_stretch]

        # Create image object
        self.image = Image.new('RGB', (self.image_side, self.image_side))
        self.draw = ImageDraw.Draw(self.image)

        # self.make_directory()

        # Create an instance of the image.
        self.get_background_colors()

        self.get_grey_tones()
        self.get_green_tones()
        self.get_gold_tones()

        while self.current_frame < self.gif_frames:
            self.get_circle_colors()
            self.draw_background_square(0, 0)
            self.draw_background()
            self.draw_border_circles()
            self.draw_border_circle_halos()
            self.draw_circle()
            self.draw_long_spokes()
            self.draw_circle_border()
            self.draw_gate_platforms()
            self.draw_gate_objects()
            self.draw_short_spokes()
            self.draw_squares()
            self.draw_box_arcs()
            self.draw_inner_square_pattern()
            self.draw_square_outlines()
            self.draw_center_shape()
            self.draw_image_heart()

            self.change_posterize_bits()
            self.apply_image_effects()

            self.save_image()

            self.change_border_circle_halo_position()
            self.change_circle_hue_count()
            self.change_circle_line_width()
            self.change_spoke_position()
            self.change_inner_square_pattern_stretch()

            self.change_current_frame()

            self.reset_settings()

    def get_background_colors(self):
        """A method to prepare the colors used in the background."""

        bg_start_color = [0, 0, 10]

        self.background_colors.append((bg_start_color[0], bg_start_color[1], bg_start_color[2]))

        for i in range(self.background_hue_count):
            bg_start_color[0] += 0
            bg_start_color[1] += 1
            bg_start_color[2] += 1
            self.background_colors.append((bg_start_color[0], bg_start_color[1], bg_start_color[2]))

    def get_circle_colors(self):
        """A method to prepare the colors used in the foreground circle."""

        circle_start_color = [200, 100, 100]
        circle_end_color = [200, 350, 155]
        circle_color_increment = [(circle_end_color[0] - circle_start_color[0]) / self.circle_hue_count,
                                  (circle_end_color[1] - circle_start_color[1]) / self.circle_hue_count,
                                  (circle_end_color[2] - circle_start_color[2]) / self.circle_hue_count]

        self.circle_colors.append((circle_start_color[0], circle_start_color[1], circle_start_color[2]))

        for i in range(self.circle_hue_count):
            circle_start_color[0] += circle_color_increment[0]
            circle_start_color[1] += circle_color_increment[1]
            circle_start_color[2] += circle_color_increment[2]
            self.circle_colors.append((int(circle_start_color[0]), int(circle_start_color[1]), int(circle_start_color[2])))

    def get_grey_tones(self):
        """A method to create a grey color tone set."""

        grey_start_color = [10, 20, 30]
        grey_end_color = [70, 120, 140]
        grey_increment = [(grey_end_color[0] - grey_start_color[0]) / self.grey_hue_count,
                          (grey_end_color[1] - grey_start_color[1]) / self.grey_hue_count,
                          (grey_end_color[2] - grey_start_color[2]) / self.grey_hue_count]

        self.grey_tones.append((grey_start_color[0], grey_start_color[1], grey_start_color[2]))

        for i in range(self.grey_hue_count):
            grey_start_color[0] += grey_increment[0]
            grey_start_color[1] += grey_increment[1]
            grey_start_color[2] += grey_increment[2]
            self.grey_tones.append((int(grey_start_color[0]), int(grey_start_color[1]), int(grey_start_color[2])))

    def get_green_tones(self):
        """A method to create a grey color tone set."""

        green_start_color = [50, 65, 50]
        green_end_color = [80, 120, 80]
        green_increment = [(green_end_color[0] - green_start_color[0]) / self.green_hue_count,
                          (green_end_color[1] - green_start_color[1]) / self.green_hue_count,
                          (green_end_color[2] - green_start_color[2]) / self.green_hue_count]

        self.green_tones.append((green_start_color[0], green_start_color[1], green_start_color[2]))

        for i in range(self.green_hue_count):
            green_start_color[0] += green_increment[0]
            green_start_color[1] += green_increment[1]
            green_start_color[2] += green_increment[2]
            self.green_tones.append((int(green_start_color[0]), int(green_start_color[1]), int(green_start_color[2])))

    def get_gold_tones(self):
        """A method to create a grey color tone set."""

        gold_start_color = [150, 140, 20]
        gold_end_color = [240, 230, 180]
        gold_increment = [(gold_end_color[0] - gold_start_color[0]) / self.gold_hue_count,
                          (gold_end_color[1] - gold_start_color[1]) / self.gold_hue_count,
                          (gold_end_color[2] - gold_start_color[2]) / self.gold_hue_count]

        self.gold_tones.append((gold_start_color[0], gold_start_color[1], gold_start_color[2]))

        for i in range(self.gold_hue_count):
            gold_start_color[0] += gold_increment[0]
            gold_start_color[1] += gold_increment[1]
            gold_start_color[2] += gold_increment[2]
            self.gold_tones.append((int(gold_start_color[0]), int(gold_start_color[1]), int(gold_start_color[2])))

    def draw_background_square(self, i, j):
        """A method to draw the reoccurring sqaure pattern in the background."""

        num = 0
        while num < 1:
            for color in self.background_colors:
                self.draw.rectangle([((i + self.background_hue_count) - num, (j + self.background_hue_count) - num),
                                     ((i + self.background_hue_count) + num, (j + self.background_hue_count) + num)],
                                    outline=color, width=1)
                num += 1

    def draw_background(self):
        """A method to draw the full background."""

        for i in range(0, self.image_side, self.background_pattern_size):
            for j in range(0, self.image_side, self.background_pattern_size):
                self.draw_background_square(i, j)

    def draw_single_border_circle(self, nw_x, nw_y, se_x, se_y, border_circle_shrink, line_distance, line_width):
        """Draws a single central circle of the border circles."""

        for i in range(0, int(self.circle_hue_count)):
            for color in self.gold_tones[12:24]:
                self.draw.ellipse((nw_x + border_circle_shrink, nw_y + border_circle_shrink,
                                   se_x - border_circle_shrink, se_y - border_circle_shrink),
                                  outline=color, width=line_width)
                border_circle_shrink += line_distance

    def draw_border_circles(self):
        """A method that calls the function draw_single_border_circle to draw all four border circles."""

        ints = [self.circle_to_image_edge / 2,
                self.circle_to_image_edge * 2,
                self.circle_to_image_edge * 2.5]

        self.draw_single_border_circle(ints[0], ints[0], ints[0] + ints[1],
                                       ints[0] + ints[1],
                                       1, 3, 1)
        self.draw_single_border_circle(self.image_side - ints[2], self.image_side - ints[2],
                                       self.image_side - ints[0], self.image_side - ints[0],
                                       1, 3, 1)
        self.draw_single_border_circle(self.image_side - ints[2], ints[0],
                                       self.image_side - ints[0], ints[0] + ints[1],
                                       1, 3, 1)
        self.draw_single_border_circle(ints[0], self.image_side - ints[2],
                                       ints[0] + ints[1], self.image_side - ints[0],
                                       1, 3, 1)

    def change_halo_spin_direction(self):
        if self.halo_spin_direction == 0:
            self.halo_spin_direction = 1
        elif self.halo_spin_direction == 1:
            self.halo_spin_direction = 0

    def draw_border_circle_halos(self):
        """A method to draw the halos surrounding each border circle."""

        arc_angles = [0, 60]

        arc_ints = [10, 15, 19, 22, 25]
        arc_ints_index = 0

        arc_inc = [0, 8, 12, 15, 19]
        arc_inc_index = 0

        green_tones = []
        green_tones_list = [12, 9, 6, 4, 2]
        for num in green_tones_list:
            green_tones.append(self.green_tones[num])
        green_tones_index = 0

        line_width = [5, 4, 3, 2, 2]
        line_width_index = 0

        spin_direction = [self.halo_spin_clockwise, self.halo_spin_counterclockwise]

        for i in range(3):
            # This loop draws one-third of the halos around each border circle,
            # drawing another one-third upon each iteration.

            for j in range(4):
                # This loop draws one-third of the halos around each border circle,
                # adding another ring outward upon each iteration.

                # Upper left border circle halos
                self.draw.arc((self.circle_to_image_edge / 2 - arc_ints[arc_ints_index],
                               self.circle_to_image_edge / 2 - arc_ints[arc_ints_index],
                               self.circle_to_image_edge * 2.5 + arc_ints[arc_ints_index],
                               self.circle_to_image_edge * 2.5 + arc_ints[arc_ints_index]),
                              arc_angles[0] + arc_inc[arc_inc_index] + spin_direction[self.halo_spin_direction],
                              arc_angles[1] - arc_inc[arc_inc_index] + spin_direction[self.halo_spin_direction],
                              fill=green_tones[green_tones_index],
                              width=line_width[line_width_index])
                arc_ints_index += 1
                arc_inc_index += 1
                green_tones_index += 1
                line_width_index += 1
                self.change_halo_spin_direction()

            arc_ints_index = 0
            arc_inc_index = 0
            green_tones_index = 0
            line_width_index = 0
            self.halo_spin_direction = 0

            for j in range(4):

                # Upper right border circle halos
                self.draw.arc((self.image_side - self.circle_to_image_edge * 2.5 - arc_ints[arc_ints_index],
                               self.circle_to_image_edge / 2 - arc_ints[arc_ints_index],
                               self.image_side - self.circle_to_image_edge / 2 + arc_ints[arc_ints_index],
                               self.circle_to_image_edge * 2.5 + arc_ints[arc_ints_index]),
                              arc_angles[0] + arc_inc[arc_inc_index] + spin_direction[self.halo_spin_direction],
                              arc_angles[1] - arc_inc[arc_inc_index] + spin_direction[self.halo_spin_direction],
                              fill=green_tones[green_tones_index],
                              width=line_width[line_width_index])
                arc_ints_index += 1
                arc_inc_index += 1
                green_tones_index += 1
                line_width_index += 1
                self.change_halo_spin_direction()

            arc_ints_index = 0
            arc_inc_index = 0
            green_tones_index = 0
            line_width_index = 0
            self.halo_spin_direction = 1

            for j in range(4):

                # Bottom right border circle halos
                self.draw.arc((self.image_side - self.circle_to_image_edge * 2.5 - arc_ints[arc_ints_index],
                               self.image_side - self.circle_to_image_edge * 2.5 - arc_ints[arc_ints_index],
                               self.image_side - self.circle_to_image_edge / 2 + arc_ints[arc_ints_index],
                               self.image_side - self.circle_to_image_edge / 2 + arc_ints[arc_ints_index]),
                              arc_angles[0] + arc_inc[arc_inc_index] + spin_direction[self.halo_spin_direction],
                              arc_angles[1] - arc_inc[arc_inc_index] + spin_direction[self.halo_spin_direction],
                              fill=green_tones[green_tones_index],
                              width=line_width[line_width_index])
                arc_ints_index += 1
                arc_inc_index += 1
                green_tones_index += 1
                line_width_index += 1
                self.change_halo_spin_direction()

            arc_ints_index = 0
            arc_inc_index = 0
            green_tones_index = 0
            line_width_index = 0
            self.halo_spin_direction = 0

            for j in range(4):

                # Bottom left border circle halos
                self.draw.arc((self.circle_to_image_edge / 2 - arc_ints[arc_ints_index],
                               self.image_side - self.circle_to_image_edge * 2.5 - arc_ints[arc_ints_index],
                               self.circle_to_image_edge * 2.5 + arc_ints[arc_ints_index],
                               self.image_side - self.circle_to_image_edge / 2 + arc_ints[arc_ints_index]),
                              arc_angles[0] + arc_inc[arc_inc_index] + spin_direction[self.halo_spin_direction],
                              arc_angles[1] - arc_inc[arc_inc_index] + spin_direction[self.halo_spin_direction],
                              fill=green_tones[green_tones_index],
                              width=line_width[line_width_index])
                arc_ints_index += 1
                arc_inc_index += 1
                green_tones_index += 1
                line_width_index += 1
                self.change_halo_spin_direction()

            arc_ints_index = 0
            arc_inc_index = 0
            green_tones_index = 0
            line_width_index = 0
            self.halo_spin_direction = 1

            arc_angles[0] += 120
            arc_angles[1] += 120

    def draw_circle(self):
        """Draws the central image."""

        for i in range(0, int(self.circle_size)):
            for color in reversed(self.circle_colors):
                self.draw.ellipse((
                    # Upper-left corner of ellipse box x-axis.
                    self.circle_to_image_edge
                    + (self.circle_shrink / self.circle_horizontal_stretch),
                    # Upper-left corner of ellipse box y-axis.
                    self.circle_to_image_edge
                    + (self.circle_shrink / self.circle_vertical_stretch),
                    # Bottom-right corner of ellipse box x-axis.
                    (self.image_side - self.circle_to_image_edge)
                    - (self.circle_shrink / self.circle_horizontal_stretch),
                    # Bottom-right corner of ellipse box y-axis.
                    (self.image_side - self.circle_to_image_edge)
                    - (self.circle_shrink / self.circle_vertical_stretch)),
                    outline=color, width=self.circle_line_width)
                self.circle_shrink += self.circle_line_distance

    def draw_long_spokes(self):
        """A method to draw the long spokes that move clockwise."""

        long_spoke_angle = 0
        for i in range(0, 12):
            self.draw.pieslice([(self.circle_to_image_edge, self.circle_to_image_edge),
                                (self.image_side - self.circle_to_image_edge,
                                 self.image_side - self.circle_to_image_edge)],
                               0 + long_spoke_angle + self.spoke_spin_clockwise,
                               2 + long_spoke_angle + self.spoke_spin_clockwise,
                               fill=self.grey_tones[10])
            long_spoke_angle += 30

    def draw_short_spokes(self):
        """A method to draw the short spokes that move counter-clockwise."""

        short_spoke_angle = 15
        short_spoke_starting_point = self.image_center - (self.square_diagonal / 2)
        for i in range(0, 12):
            self.draw.pieslice([(short_spoke_starting_point, short_spoke_starting_point),
                                (self.image_side - short_spoke_starting_point,
                                 self.image_side - short_spoke_starting_point)],
                               0 + short_spoke_angle + self.spoke_spin_counterclockwise,
                               4 + short_spoke_angle + self.spoke_spin_counterclockwise,
                               fill=self.grey_tones[5])
            short_spoke_angle += 30

    def draw_single_square(self, distance_from_center, color_set, color):
        """A method to define one of the squares."""

        ints = []
        for i in range(1):
            ints.append(self.image_center - distance_from_center)
            ints.append(self.image_center + distance_from_center)

        self.draw.polygon(((ints[0], ints[0]), (ints[1], ints[0]),
                           (ints[1], ints[1]), (ints[0], ints[1])),
                          fill=color_set[color])

    def draw_squares(self):
        """A method to draw all the squares."""

        self.draw_single_square(self.shape_ints[4] + self.shape_ints[1], self.grey_tones, 6)
        self.draw_single_square(self.shape_ints[4], self.gold_tones, 18)
        self.draw_single_square(self.shape_ints[4] - ((self.shape_ints[4] - self.shape_ints[2]) / 3), self.grey_tones, 12)
        self.draw_single_square(self.shape_ints[4] - ((self.shape_ints[4] - self.shape_ints[2]) / 1.5), self.gold_tones, 18)
        self.draw_single_square(self.shape_ints[2], self.grey_tones, 6)

    def draw_square_outline(self, distance_from_center, color, border_width):
        """A method to define one of the square outlines. """

        ints = []
        for i in range(1):
            ints.append(self.image_center - distance_from_center)
            ints.append(self.image_center + distance_from_center)

        self.draw.line([(ints[0], ints[0]), (ints[1], ints[0]), (ints[1], ints[1]),
                        (ints[0], ints[1]), (ints[0], ints[0])],
                       fill=self.grey_tones[color], width=border_width)

    def draw_square_outlines(self):
        """A method to draw all the square outlines."""

        self.draw_square_outline(self.shape_ints[4] + self.shape_ints[1], 0, 3)
        self.draw_square_outline(self.shape_ints[4], 0, 3)
        self.draw_square_outline(self.shape_ints[4] - ((self.shape_ints[4] - self.shape_ints[2]) / 3), 0, 3)
        self.draw_square_outline(self.shape_ints[4] - ((self.shape_ints[4] - self.shape_ints[2]) / (3 / 2)), 0, 3)
        self.draw_square_outline(self.shape_ints[2], 0, 3)

    def draw_center_shape(self):
        """A method to draw the shape within the center squares."""

        ints = []
        for i in range(5):
            ints.append(self.image_center - self.shape_ints[i])
        for i in range(5):
            ints.append(self.image_center + self.shape_ints[i])

        self.draw.polygon((
            # Top side of the shape.
            (ints[0], ints[0]), (ints[1], ints[0]), (ints[1], ints[2]), (ints[3], ints[2]), (ints[3], ints[4]),
            (ints[8], ints[4]), (ints[8], ints[2]), (ints[6], ints[2]), (ints[6], ints[0]),
            # Right side of the shape.
            (ints[5], ints[0]), (ints[5], ints[1]), (ints[7], ints[1]), (ints[7], ints[3]), (ints[9], ints[3]),
            (ints[9], ints[8]), (ints[7], ints[8]), (ints[7], ints[6]), (ints[5], ints[6]),
            # Bottom side of the shape.
            (ints[5], ints[5]), (ints[6], ints[5]), (ints[6], ints[7]), (ints[8], ints[7]), (ints[8], ints[9]),
            (ints[3], ints[9]), (ints[3], ints[7]), (ints[1], ints[7]), (ints[1], ints[5]),
            # Left side of the shape.
            (ints[0], ints[5]), (ints[0], ints[6]), (ints[2], ints[6]), (ints[2], ints[8]), (ints[4], ints[8]),
            (ints[4], ints[3]), (ints[2], ints[3]), (ints[2], ints[1]), (ints[0], ints[1]),
        ),
            fill=self.grey_tones[20], outline=self.grey_tones[4])

    def draw_image_heart(self):
        """A method to draw the innermost object of the image."""

        arc_angle1 = 356
        arc_angle2 = 4
        heart_ints = [230, 210, 190, 170, 150]
        for i in range(12):
            div_rate = 1
            speed_increase = 1
            gold_tone1 = 0
            gold_tone2 = 8
            for heart_int in heart_ints:
                # The outer shell
                self.draw.arc((self.image_center - heart_int, self.image_center - heart_int,
                               self.image_center + heart_int, self.image_center + heart_int),
                              arc_angle1 + (self.spoke_spin_clockwise * speed_increase),
                              arc_angle2 + (self.spoke_spin_clockwise * speed_increase),
                              fill=self.gold_tones[gold_tone1], width=10)
                self.draw.arc((self.image_center - heart_int + 10, self.image_center - heart_int + 10,
                               self.image_center + heart_int - 10, self.image_center + heart_int - 10),
                              arc_angle1 + (self.spoke_spin_counterclockwise * speed_increase),
                              arc_angle2 + (self.spoke_spin_counterclockwise * speed_increase),
                              fill=self.gold_tones[gold_tone2], width=10)
                speed_increase += 1
                gold_tone1 += 3
                gold_tone2 += 3
            for j in range(5):
                # The horizontal ellipse
                self.draw.arc((self.image_center - 120 * div_rate, self.image_center - 40 * div_rate,
                               self.image_center + 120 * div_rate, self.image_center + 40 * div_rate),
                              arc_angle1 + self.spoke_spin_clockwise * 2,
                              arc_angle2 + self.spoke_spin_clockwise * 2,
                              fill=self.grey_tones[16], width=5)
                self.draw.arc((self.image_center - 90 * div_rate, self.image_center - 25 * div_rate,
                               self.image_center + 90 * div_rate, self.image_center + 25 * div_rate),
                              arc_angle1 + self.spoke_spin_counterclockwise * 2,
                              arc_angle2 + self.spoke_spin_counterclockwise * 2,
                              fill=self.grey_tones[16], width=5)
                # The vertical ellipse
                self.draw.arc((self.image_center - 40 * div_rate, self.image_center - 120 * div_rate,
                               self.image_center + 40 * div_rate, self.image_center + 120 * div_rate),
                              arc_angle1 + self.spoke_spin_clockwise * 2,
                              arc_angle2 + self.spoke_spin_clockwise * 2,
                              fill=self.grey_tones[16], width=5)
                self.draw.arc((self.image_center - 25 * div_rate, self.image_center - 90 * div_rate,
                               self.image_center + 25 * div_rate, self.image_center + 90 * div_rate),
                              arc_angle1 + self.spoke_spin_counterclockwise * 2,
                              arc_angle2 + self.spoke_spin_counterclockwise * 2,
                              fill=self.grey_tones[16], width=5)
                div_rate = div_rate * 0.9
            arc_angle1 += 30
            arc_angle2 += 30

    def draw_circle_border(self):
        """A method to draw the circle border."""

        arc_size = 0
        fill = 0
        for i in range(0, 30, 1):
            self.draw.arc((self.circle_to_image_edge + arc_size,
                           self.circle_to_image_edge + arc_size,
                           self.image_side - self.circle_to_image_edge - arc_size,
                           self.image_side - self.circle_to_image_edge - arc_size),
                          0, 360, fill=self.green_tones[fill], width=4)
            arc_size += 4
            if arc_size % 10 == 0:
                fill += 4

    def draw_gate_platforms(self):
        """A method to draw the gates."""

        ints = []
        for i in range(5):
            ints.append(self.image_center - self.shape_ints[i])
        for i in range(5):
            ints.append(self.image_center + self.shape_ints[i])
        ints.append(self.shape_ints[4] - self.shape_ints[2])

        color_list = [(35, 20, 20), (45, 24, 24), (55, 28, 28)]
        num = 1
        for color in reversed(color_list):
            for i in range(0, 3):
                # Draw the gate platform above the shape.
                self.draw.rectangle(
                    (ints[3] - (((ints[10]) / 3) * num),
                     ints[4] - (self.shape_ints[1] * 3.5) + (((ints[10]) / 3) * num),
                     ints[8] + (((ints[10]) / 3) * num),
                     ints[4] - self.shape_ints[1]),
                    fill=color)
                # Draw the gate platform to the right of the shape.
                self.draw.rectangle(
                    (ints[9] + (self.shape_ints[1] * 1),
                     ints[3] - (((ints[10]) / 3) * num),
                     ints[9] + (self.shape_ints[1] * 3.5) - (((ints[10]) / 3) * num),
                     ints[8] + (((ints[10]) / 3) * num)),
                    fill=color)
                # Draw the gate platform below the shape.
                self.draw.rectangle(
                    (ints[3] - (((ints[10]) / 3) * num),
                     ints[9] + self.shape_ints[1],
                     ints[8] + (((ints[10]) / 3) * num),
                     ints[9] + (self.shape_ints[1] * 3.5) - (((ints[10]) / 3) * num)),
                    fill=color)
                # Draw the gate platform to the left of the shape.
                self.draw.rectangle(
                    (ints[4] - (self.shape_ints[1] * 3.5) + (((ints[10]) / 3) * num),
                     ints[3] - (((ints[10]) / 3) * num),
                     ints[4] - (self.shape_ints[1] * 1),
                     ints[8] + (((ints[10]) / 3) * num)),
                    fill=color)
            num += 1

    def draw_gate_objects(self):
        """A method to draw the objects that sit upon the gate platforms."""

        # The supporting pillar.
        ints_0 = []
        for i in range(15, 31, 15):
            ints_0.append(self.image_center - i)
        for i in range(15, 31, 15):
            ints_0.append(self.image_center + i)
        ints_0.append(self.image_side - self.platform_int)
        self.draw.rectangle((ints_0[0], self.platform_int - 30, ints_0[2], self.platform_int), fill=self.gold_tones[6])
        self.draw.rectangle((ints_0[4], ints_0[0], ints_0[4] + 30, ints_0[2]), fill=self.gold_tones[6])
        self.draw.rectangle((ints_0[0], ints_0[4], ints_0[2], ints_0[4] + 30), fill=self.gold_tones[6])
        self.draw.rectangle((self.platform_int - 30, ints_0[0], self.platform_int, ints_0[2]), fill=self.gold_tones[6])

        # Shading on the supporting pillar.
        line_growth = 1
        for i in range(1):
            ints_01 = [self.image_center - 16 + i + line_growth, self.image_center + 16 - i - line_growth,
                       self.platform_int - 30, self.image_side - self.platform_int + 30]
            for color in reversed(self.gold_tones[8:17]):
                self.draw.line((ints_01[0], self.platform_int, ints_01[0], ints_01[2]), fill=color)
                self.draw.line((self.image_side - self.platform_int, ints_01[0], ints_01[3], ints_01[0]), fill=color)
                self.draw.line((ints_01[1], self.image_side - self.platform_int, ints_01[1], ints_01[3]), fill=color)
                self.draw.line((ints_01[2], ints_01[1], self.platform_int, ints_01[1]), fill=color)
                line_growth *= 1.5

        # The large lower bowl.
        ints_02_list = [28, 60]
        ints_02 = [self.image_center - 30, self.image_center + 30]
        for i in ints_02_list:
            ints_02.append(self.platform_int - i)
            ints_02.append(self.image_side - self.platform_int + i)

        self.draw.chord((ints_02[0], ints_02[4], ints_02[1], ints_02[2]),
                        360, 180, fill=self.gold_tones[4])
        self.draw.chord((ints_02[3], ints_02[0], ints_02[5], ints_02[1]),
                        90, 270, fill=self.gold_tones[4])
        self.draw.chord((ints_02[0], ints_02[3], ints_02[1], ints_02[5]),
                        180, 360, fill=self.gold_tones[4])
        self.draw.chord((ints_02[4], ints_02[0], ints_02[2], ints_02[1]),
                        270, 90, fill=self.gold_tones[4])

        # The three smaller bowls.
        ints_03 = []
        ints_03a_list = [15, 40]
        ints_03b_list = [44, 70]
        for i in ints_03a_list:
            ints_03.append(self.image_center - i)
            ints_03.append(self.image_center + i)
        for i in ints_03b_list:
            ints_03.append(self.platform_int - i)
            ints_03.append(self.image_side - self.platform_int + i)
        for i in range(3):
            self.draw.chord((ints_03[2], ints_03[6], ints_03[0], ints_03[4]),
                            360, 180, fill=self.gold_tones[6])
            self.draw.chord((ints_03[5], ints_03[2], ints_03[7], ints_03[0]),
                            90, 270, fill=self.gold_tones[6])
            self.draw.chord((ints_03[1], ints_03[5], ints_03[3], ints_03[7]),
                            180, 360, fill=self.gold_tones[6])
            self.draw.chord((ints_03[6], ints_03[1], ints_03[4], ints_03[3]),
                            270, 90, fill=self.gold_tones[6])
            ints_03[0] += 27
            ints_03[1] -= 27
            ints_03[2] += 27
            ints_03[3] -= 27

        # The upper platform.
        ints_04_list = [58, 65]
        ints_04 = [self.image_center - 45, self.image_center + 45]
        for i in ints_04_list:
            ints_04.append(self.platform_int - i)
            ints_04.append(self.image_side - self.platform_int + i)
        self.draw.rectangle((ints_04[0], ints_04[4], ints_04[1], ints_04[2]),
                            fill=self.gold_tones[0])
        self.draw.rectangle((ints_04[3], ints_04[0], ints_04[5], ints_04[1]),
                            fill=self.gold_tones[0])
        self.draw.rectangle((ints_04[0], ints_04[3], ints_04[1], ints_04[5]),
                            fill=self.gold_tones[0])
        self.draw.rectangle((ints_04[4], ints_04[0], ints_04[2], ints_04[1]),
                            fill=self.gold_tones[0])

        # Shading for the upper platform.
        line_growth = 1
        ints_05_list = [46, 58, 65]
        ints_05 = [self.image_center - ints_05_list[0], self.image_center + ints_05_list[0],
                   self.platform_int - ints_05_list[1], self.platform_int - ints_05_list[2],
                   self.image_side - self.platform_int + ints_05_list[1],
                   self.image_side - self.platform_int + ints_05_list[2]]
        for color in reversed(self.gold_tones[1:15]):
            self.draw.line((ints_05[0] + line_growth, ints_05[3], ints_05[0] + line_growth, ints_05[2]),
                        fill=color)
            self.draw.line((ints_05[4], ints_05[0] + line_growth, ints_05[5], ints_05[0] + line_growth),
                        fill=color)
            self.draw.line((ints_05[1] - line_growth, ints_05[4], ints_05[1] - line_growth, ints_05[5]),
                        fill=color)
            self.draw.line((ints_05[3], ints_05[1] - line_growth, ints_05[2], ints_05[1] - line_growth),
                        fill=color)
            line_growth *= 1.4

        # The hovering circle.
        ints_06_list = [70, 110]
        ints_06 = [self.image_center - 20, self.image_center + 20]
        for i in ints_06_list:
            ints_06.append(self.platform_int - i)
            ints_06.append(self.image_side - self.platform_int + i)
        self.draw.ellipse((ints_06[0], ints_06[4], ints_06[1], ints_06[2]),
                          fill=self.gold_tones[14])
        self.draw.ellipse((ints_06[3], ints_06[0], ints_06[5], ints_06[1]),
                          fill=self.gold_tones[14])
        self.draw.ellipse((ints_06[0], ints_06[3], ints_06[1], ints_06[5]),
                          fill=self.gold_tones[14])
        self.draw.ellipse((ints_06[4], ints_06[0], ints_06[2], ints_06[1]),
                          fill=self.gold_tones[14])

    def draw_box_arcs(self):
        """A method to fill the boxes with a repeating arc pattern."""

        fill = [self.green_tones[2], self.green_tones[8]]

        ints_07 = []
        for i in [2, 4]:
            ints_07.append(self.image_center - self.shape_ints[i])
            ints_07.append(self.image_center + self.shape_ints[i])
        ints_07.append((self.shape_ints[4] - self.shape_ints[2]) / 1.5)
        ints_07.append((self.shape_ints[4] - self.shape_ints[2]) / 3)
        
        for i in range(0, int(self.shape_ints[4] * 2) - 25, int((self.shape_ints[4] * 2) / 45)):
            # Outer pattern above the shape.
            self.draw.arc((ints_07[2] + i,
                           ints_07[2],
                           self.image_center - (
                                       self.shape_ints[4] - ints_07[4]) + i,
                           self.image_center - (
                                       self.shape_ints[4] - ints_07[4])),
                          180, 360, fill=fill[0], width=2)
            # Outer pattern to the right of the shape.
            self.draw.arc((ints_07[3] - ints_07[4],
                           ints_07[2] + i,
                           ints_07[3],
                           ints_07[2] + ints_07[4] + i),
                          270, 90, fill=fill[0], width=2)
            # Outer pattern below the shape.
            self.draw.arc((ints_07[3] - ints_07[4] - i,
                           ints_07[3] - ints_07[4],
                           ints_07[3] - i,
                           ints_07[3]),
                360, 180, fill=fill[0], width=2)
            # Outer pattern to the left of the shape.
            self.draw.arc((ints_07[2],
                           ints_07[3] - ints_07[4] - i,
                           ints_07[2] + ints_07[4],
                           ints_07[3] - i),
                          90, 270, fill=fill[0], width=2)

        for i in range(0, int((self.shape_ints[4] - ints_07[4]) * 2 - 35),
                       int((self.shape_ints[4] * 2) / 45)):
            # Inner pattern above the shape.
            self.draw.arc((ints_07[0] - ints_07[5] + i,
                           ints_07[0] - ints_07[4],
                           ints_07[0] + ints_07[5] + i,
                           ints_07[0]),
                          360, 180, fill=fill[1], width=3)
            # Inner pattern to the right of the shape.
            self.draw.arc((ints_07[1],
                           ints_07[0] - ints_07[5] + i,
                           ints_07[1] + ints_07[4],
                           ints_07[0] + ints_07[5] + i),
                          90, 270, fill=fill[1], width=3)
            # Inner pattern below the shape.
            self.draw.arc((ints_07[1] - ints_07[5] - i,
                           ints_07[1],
                           ints_07[1] + ints_07[5] - i,
                           ints_07[1] + ints_07[4]),
                          180, 360, fill=fill[1], width=3)
            # Inner pattern to the left of the shape.
            self.draw.arc((ints_07[0] - ints_07[4],
                           ints_07[1] - ints_07[5] - i,
                           ints_07[0],
                           ints_07[1] + ints_07[5] - i),
                          270, 90, fill=fill[1], width=3)

    def draw_inner_square_pattern(self):
        """A method to draw the pattern in the innermost square."""

        ints_08 = []
        for i in [0, 2]:
            ints_08.append(self.image_center - self.shape_ints[i])
            ints_08.append(self.image_center + self.shape_ints[i])

        for i in range(0, int((self.image_center - self.shape_ints[2]) / 2), 10 + self.inner_square_pattern_stretch):
            # Pattern above the shape.
            self.draw.polygon(((ints_08[2] + i, ints_08[2]),
                               (ints_08[0] + i, ints_08[0]),
                               (ints_08[0] + i, ints_08[2])),
                              outline=self.circle_colors[5])
            self.draw.polygon(((ints_08[3] - i, ints_08[2]),
                               (ints_08[1] - i, ints_08[0]),
                               (ints_08[1] - i, ints_08[2])),
                              outline=self.circle_colors[5])
            # Pattern to the right of the shape.
            self.draw.polygon(((ints_08[3], ints_08[2] + i),
                               (ints_08[1], ints_08[0] + i),
                               (ints_08[3], ints_08[0] + i)),
                              outline=self.circle_colors[5])
            self.draw.polygon(((ints_08[3], ints_08[3] - i),
                               (ints_08[1], ints_08[1] - i),
                               (ints_08[3], ints_08[1] - i)),
                              outline=self.circle_colors[5])
            # Pattern below the shape.
            self.draw.polygon(((ints_08[3] - i, ints_08[3]),
                               (ints_08[1] - i, ints_08[1]),
                               (ints_08[1] - i, ints_08[3])),
                              outline=self.circle_colors[5])
            self.draw.polygon(((ints_08[2] + i, ints_08[3]),
                               (ints_08[0] + i, ints_08[1]),
                               (ints_08[0] + i, ints_08[3])),
                              outline=self.circle_colors[5])
            # Pattern to the left of the shape.
            self.draw.polygon(((ints_08[2], ints_08[3] - i),
                               (ints_08[0], ints_08[1] - i),
                               (ints_08[2], ints_08[1] - i)),
                              outline=self.circle_colors[5])
            self.draw.polygon(((ints_08[2], ints_08[2] + i),
                               (ints_08[0], ints_08[0] + i),
                               (ints_08[2], ints_08[0] + i)),
                              outline=self.circle_colors[5])

    def change_border_circle_halo_position(self):
        """A method to change the direction of the border circle halos."""

        self.halo_spin_clockwise += 4
        self.halo_spin_counterclockwise -= 4

    def change_circle_hue_count(self):
        """A method to change the circle hues between frames of the GIF."""

        self.circle_hue_count += self.circle_hue_count_growth
        if self.circle_hue_count == 25:
            self.change_circle_hue_count_direction()
        elif self.circle_hue_count == 10:
            self.change_circle_hue_count_direction()

    def change_circle_hue_count_direction(self):
        """A method to change the direction of the circle hue count."""

        self.circle_hue_count_growth = self.circle_hue_count_growth * -1

    def change_circle_line_width(self):
        """When creating a GIF, makes the circle line width shrink and grow."""

        self.circle_line_width += self.circle_line_width_growth
        if self.circle_line_width == 6:
            self.change_circle_line_width_direction()
        elif self.circle_line_width == 1:
            self.change_circle_line_width_direction()

    def change_circle_line_width_direction(self):
        """A method to change the direction of the circle line width."""

        self.circle_line_width_growth = self.circle_line_width_growth * -1

    def change_spoke_position(self):
        """A method to make the circle spokes spin."""

        self.spoke_spin_clockwise += 1
        self.spoke_spin_counterclockwise -= 1

    def change_inner_square_pattern_stretch(self):
        """When creating a GIF, makes the inner square pattern shrink and grow."""

        self.inner_square_pattern_stretch += self.inner_square_pattern_growth
        if self.inner_square_pattern_stretch == 20:
            self.change_inner_square_pattern_direction()
        elif self.inner_square_pattern_stretch == 5:
            self.change_inner_square_pattern_direction()

    def change_inner_square_pattern_direction(self):
        """A method to change the direction of the inner square pattern growth."""

        self.inner_square_pattern_growth = self.inner_square_pattern_growth * -1

    def change_posterize_bits(self):
        """A method to change posterization bits."""

        if 18 > self.current_frame >= 10:
            self.posterize_bits -= 1
        elif 26 > self.current_frame >= 18:
            self.posterize_bits += 1
        elif self.current_frame >= 26:
            pass

    def apply_image_effects(self):
        """Apply image sharpening and posterization effects."""

        self.image_mask = self.image.filter(ImageFilter.UnsharpMask(radius=7, percent=75))
        self.image_effects = ImageOps.posterize(self.image_mask, bits=self.posterize_bits)

    def change_current_frame(self):
        """Progresses to the next GIF frame."""

        self.current_frame += 1

    def reset_settings(self):
        """A method to reset settings in the __init__ method."""

        self.background_pattern_count = self.settings_list[0]
        self.border_circle_divisor = self.settings_list[1]
        self.circle_shrink = self.settings_list[2]
        self.circle_line_distance = self.settings_list[3]

    def save_image(self):
        """Save the image and apply image effects."""

        folder_path = Path.cwd()

        test = os.listdir(folder_path)

        if self.current_frame < 10:
            self.image_effects.save(f'Mandala-0{self.current_frame}.png')
        else:
            self.image_effects.save(f'Mandala-{self.current_frame}.png')

        print(f"Creating frame {self.current_frame} of {self.frame_count}...")


class GifCreator:
    """Overall class to create the GIF from the image frames."""

    def __init__(self):
        """A method to control settings for the GIF, as well as run all class methods."""

        self.frame_duration = 0.08

        self.create_gif()

    def create_gif(self):
        """A method to create the GIF."""

        print("\nCreating the GIF. (Almost done...)")

        file_names = sorted((fn for fn in os.listdir('.') if fn.endswith('.png')))
        with io.get_writer('Mandala-GIF.gif', mode='I', duration=self.frame_duration) as writer:
            for filename in file_names:
                if filename == 'Mandala_02-030.png':
                    continue
                image = io.imread(filename)
                writer.append_data(image)
        print("\nGIF created!")

        writer.close()


class DeleteImages:
    """A class to delete the image files."""

    def __init__(self):

        folder_path = Path.cwd()

        test = os.listdir(folder_path)

        for images in test:
            if images.endswith('.png'):
                os.remove(os.path.join(folder_path, images))


def main():
    draw = Mandala()
    gif = GifCreator()
    images = DeleteImages()


if __name__ == "__main__":
    main()
