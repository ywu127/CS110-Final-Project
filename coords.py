def coords_pixels(coords):

    pixels = []

    try:

        for a in coords:

            pixels.append(a*60)

        return tuple(pixels)

    except TypeError:

        return coords*60

def pixels_coords(pixels):

    coords = []

    try:

        for a in pixels:

            coords.append(a/60)

        return tuple(coords)

    except TypeError:

        return pixels/60

def stick_pixels(pixels):

    x = pixels[0]
    y = pixels[1]

    x_coord, y_coord = pixels_coords((x, y))

    for step in range(1, 12):

        if abs(step - x_coord) <= 0.5:

            x_stuck = coords_pixels(step)

        if abs(step - y_coord) <= 0.5:

            y_stuck = coords_pixels(step)

    return (x_stuck, y_stuck)
