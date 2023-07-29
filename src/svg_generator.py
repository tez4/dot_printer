import svgwrite

dwg = svgwrite.Drawing('./output/test.svg', (1500, 500))


dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill='#FFFFFF'))


def add_circle(dwg, position, radius, color):
    circle = svgwrite.shapes.Circle(center=position, r=radius, fill=color)
    dwg.add(circle)


add_circle(dwg, (100, 100), 80, '#FF00FF')

dwg.save()
