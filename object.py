import json

class Object:
    def __init__(self, w, h, x=0, y=0, color="black", type="normal"):
        self.w = abs(w)
        self.h = abs(h)
        self.x = float(x)
        self.y = float(y)
        self.color = str(color)
        self.type = str(type)

    def boundingbox(self):
        w, h, centerx, centery = self.w / 2, self.h / 2, self.x, self.y
        return [
            (centerx - w, centery + h),
            (centerx + w, centery + h),
            (centerx + w, centery - h),
            (centerx - w, centery - h),
        ]

def from_shapepoly(shape_poly, x=0, y=0, color="black", type="normal"):
    min_x, max_x = min(point[0] for point in shape_poly), max(
        point[0] for point in shape_poly
    )
    min_y, max_y = min(point[1] for point in shape_poly), max(
        point[1] for point in shape_poly
    )
    return Object(max_x - min_x, max_y - min_y, x, y, color, type)

def load_objects_from_file(file_name):
    try:
        with open(file_name, "r") as file:
            return [
                Object(
                    w=object["w"],
                    h=object["h"],
                    x=object["x"],
                    y=object["y"],
                    color=object["c"],
                    type=object["t"],
                )
                for object in json.load(file)
        ]
    except:
        return None

if __name__ == "__main__":
    from main import Main
    Main()