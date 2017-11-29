#!/usr/bin/env python3
#make a row that is goal inches long
#1" bricks and 5" bricks

def make_bricks(num_small, num_big, goal):
    if num_small * 1 + num_big * 5 < goal:
        return False
    needed_large = goal // 5
    if needed_large > num_big:
        return False
    needed_small = goal % 5
    if needed_small > num_small:
       return False
    print("needed_large:", needed_large)
    print("needed_small:", needed_small)

    return True


if __name__ == "__main__":
   assert make_bricks(3,1,8) is True
   assert make_bricks(3,1,9) is False
   assert make_bricks(10,0,8) is False
   assert make_bricks(3, 2, 10) is True
   print("All tests passed")
