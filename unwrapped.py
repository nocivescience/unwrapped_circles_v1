from manim import *
class UnfoldCircles(Scene):
    CONFIG = {
        "circle_style": {
            "fill_color": GREY_BROWN,
            "fill_opacity": 0,
            "stroke_color": GREY_BROWN,
            "stroke_width": 2,
        },
        "radius": 1.0,
        "dr": 0.01,
    }

    def construct(self):
        self.add_four_circles()

    def add_four_circles(self):
        radius = self.CONFIG['radius']

        radii_lines = VGroup(*[
            Line(radius * UP, ORIGIN).set_stroke(WHITE, 2)
            for x in range(1)
        ])
        radii_lines.arrange_in_grid(buff=1.3)
        radii_lines[2:].shift(RIGHT)

        unwrap_factor_tracker = ValueTracker(0)

        def get_circle(line):
            return always_redraw(
                lambda: self.get_unwrapped_circle(
                    radius=radius, dr=self.CONFIG['dr'],
                    unwrap_factor=unwrap_factor_tracker.get_value(),
                    center=line.get_top()
                )
            )

        circles = VGroup(*[get_circle(line) for line in radii_lines])
        circle_copies = circles.copy()
        for mob in circle_copies:
            mob.clear_updaters()

        self.play(
            LaggedStartMap(Write, circle_copies, lag_ratio=0.7),
            LaggedStartMap(Create, radii_lines),
        )
        self.remove(circle_copies)
        self.add(circles, radii_lines)
        self.wait()
        self.play(
            radii_lines[2:].animate.shift(2.9 * RIGHT),
        )
        self.play(
            unwrap_factor_tracker.animate.set_value(1),
            run_time=2
        )
        self.wait()

        # Move triangles
        triangles = circles.copy()
        for triangle in triangles:
            triangle.clear_updaters()
            border = Polygon(*[
                triangle.get_corner(vect)
                for vect in (DL, UL, DR)
            ])
            border.set_stroke(WHITE, 1)
            triangle.add(border)
            triangle.generate_target()
        for i, triangle in enumerate(triangles):
            if i % 2 == 1:
                triangle.target.rotate(PI)
            vect = UP if i < 2 else DOWN

        self.play(FadeIn(triangles))
        self.add(triangles, triangles.copy())
        self.play(MoveToTarget(triangles[0]))
        self.wait()
        self.play(LaggedStartMap(MoveToTarget, triangles))
        self.wait()

    #
    def get_unwrapped_circle(self, radius, dr, unwrap_factor=0, center=ORIGIN):
        radii = np.arange(0, radius + dr, dr)
        rings = VGroup()
        for r in radii:
            r_factor = 1 + 3 * (r / radius)
            alpha = unwrap_factor**r_factor
            alpha = np.clip(alpha, 0, 0.9999)
            angle = interpolate(TAU, 0, alpha)
            length = TAU * r
            arc_radius = length / angle
            ring = Arc(
                start_angle=-90 * DEGREES,
                angle=angle,
                radius=arc_radius,
                **self.CONFIG['circle_style']
            )
            ring.shift(center + (r - arc_radius) * DOWN)
            rings.add(ring)
        return rings