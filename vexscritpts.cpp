//make invisible particles outside of camera
int kill_x =  @uv.x - ch("d_x") < 0 || @uv.x < 1 * ch("d_x");
int kill_y =  @uv.y - ch("d_y") < 0 || @uv.y < 1 * ch("d_y");
i@kill = kill_x || kill_y;
@Cd = set(i@kill, 0, 1-i@kill);
