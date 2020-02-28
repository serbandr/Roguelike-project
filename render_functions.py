import tcod as libtcod
from camera import to_camera_coordinates, move_camera

def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, player, camera_width, camera_height, camera_x, camera_y, colors):
    
    camera_x, camera_y = move_camera(player.x, player.y, camera_width, camera_height, camera_y, camera_x, game_map)

    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(camera_height):
            for x in range(camera_width):
                visible = libtcod.map_is_in_fov(fov_map, camera_x + x, camera_y + y)
                wall = game_map.tiles[camera_x + x][camera_y + y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[camera_x + x][camera_y + y].explored = True
                elif game_map.tiles[camera_x + x][camera_y + y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)


    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, fov_map, camera_width, camera_height, camera_x, camera_y)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_flush()

    clear_all(con, entities, camera_width, camera_height, camera_x, camera_y)


def clear_all(con, entities, camera_width, camera_height, camera_x, camera_y):
    for entity in entities:
        clear_entity(con, entity, camera_width, camera_height, camera_x, camera_y)


def draw_entity(con, entity, fov_map, camera_width, camera_height, camera_x, camera_y):
    x, y = to_camera_coordinates(entity.x, entity.y, camera_width, camera_height, camera_x, camera_y)

    if x is not None:
        if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            libtcod.console_set_default_foreground(con, entity.color)
            libtcod.console_put_char(con, x, y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity, camera_width, camera_height, camera_x, camera_y):
    # erase the character that represents this object
    x, y = to_camera_coordinates(entity.x, entity.y, camera_width, camera_height, camera_x, camera_y)
    if x is not None:
        libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
