def check_collision(obj1, obj2):
    obj1_left = obj1.x - obj1.w / 2
    obj1_right = obj1.x + obj1.w / 2
    obj1_top = obj1.y + obj1.h / 2
    obj1_bottom = obj1.y - obj1.h / 2

    obj2_left = obj2.x - obj2.w / 2
    obj2_right = obj2.x + obj2.w / 2
    obj2_top = obj2.y + obj2.h / 2
    obj2_bottom = obj2.y - obj2.h / 2

    if (
        obj1_right > obj2_left
        and obj1_left < obj2_right
        and obj1_top > obj2_bottom
        and obj1_bottom < obj2_top
    ):
        dx_left = abs(obj1_left - obj2_right)
        dx_right = abs(obj1_right - obj2_left)
        dy_top = abs(obj1_top - obj2_bottom)
        dy_bottom = abs(obj1_bottom - obj2_top)

        min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

        if min_overlap == dx_left:
            return (obj1_left - obj2.w / 2, obj2.y)
        elif min_overlap == dx_right:
            return (obj1_right + obj2.w / 2, obj2.y)
        elif min_overlap == dy_top:
            return (obj2.x, obj1_top + obj2.h / 2)
        elif min_overlap == dy_bottom:
            return (obj2.x, obj1_bottom - obj2.h / 2)

    return None

if __name__ == "__main__":
    from main import Main
    Main()