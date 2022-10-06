from this import d
from manim import *
class UnwrappedCircle(Scene):
    CONFIG={
        
    }
    def construct(self):
        arcs=self.get_unwrapped_circle(.1)
        lines=self.get_lines()
        self.play(
            LaggedStartMap(Create,arcs),
            Create(arcs.line)
        )
        self.play(Transform(arcs,lines))
        self.wait()
    def get_unwrapped_circle(self,dr):
        line=Line(ORIGIN,2*UP)
        radio=line.get_length()
        radii=self.radii=np.arange(0,radio+dr,dr)
        arcs=VGroup()
        for r in radii:
            alpha=0
            alpha=np.clip(alpha,0,.999)
            angle=interpolate(TAU,0,alpha)
            arc=Arc(radius=r,start_angle=PI/2,angle=TAU*r/angle)#.move_to(line.points[0])
            arc.shift((r-TAU*r/angle)*DOWN)
            arcs.add(arc)
        arcs.line=line
        return arcs
    def get_lines(self):
        return VGroup(*[
            Line(TAU*radio*RIGHT+radio*UP,radio*UP) for radio in self.radii
        ])