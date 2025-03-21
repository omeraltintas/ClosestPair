import matplotlib.pyplot as plt
import matplotlib.animation as animation
import statistics as stat
import math
import mysort as mysrt

class ClosestPairProject:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
def calculate_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
def read_points(file_path):
        points=[]
        with open(file_path,'r')as file:
            for line in file:
                x,y=map(float,line.strip().split())
                points.append((x,y))
        return points

def naive_alg(p,n):
        min=float('inf')
        steps=[]
        closest_pair=(None,None)
        for i in range(n):
            for j in range(i+1,n):
                x=calculate_distance(p[i],p[j])
                steps.append((points[i],points[j],x))
                if x<min:
                        min=calculate_distance(p[i],p[j])
                        closest_pair=(points[i],points[j])
        return min,closest_pair,steps

def animate_algorithm(points,steps):
      fig,ax=plt.subplots()
      ax.set_xlim(-50,50)
      ax.set_ylim(-50,50)
      ax.set_title("CENG 383 Closest Pair")
      ax.scatter(*zip(*points), color='blue', label="Points") 
      line, = ax.plot([], [], color='red', linewidth=2, label="Current Pair")
      min_line, = ax.plot([], [], color='green', linewidth=2, label="Closest Pair")
      
      ####################  MIN DISTANCE ###########################
      min_dist_text=ax.text(0.5,0.95,"",transform=ax.transAxes, ha="center",va="top",fontsize=12)
      ####################  MIN DISTANCE ###########################

      min_dist=float('inf')
      closest_pair=(None,None)

      def update(frame):
            p1,p2,distance=steps[frame]
            line.set_data([p1[0],p2[0]],[p1[1],p2[1]])

            nonlocal min_dist,closest_pair
            if distance<min_dist:
                  min_dist=distance
                  closest_pair=(p1,p2)
                  min_line.set_data([p1[0], p2[0]], [p1[1], p2[1]])
            if frame==len(steps)-1:
                  min_dist_text.set_text(f"Min Distance: {min_dist}")
            return line,min_line,min_dist_text
      
      anim=animation.FuncAnimation(fig,update,frames=len(steps),interval=0,blit=True)
      ax.legend()
      plt.show()

def closest_strip(strip,min_distance):
      strip=mysrt.merge_sort(strip,key=lambda p:p[1])
      min_d = min_distance
      closest_pair = (None, None)
      
      for i in range(len(strip)):
            for j in range(i+1,len(strip)):
                  if (strip[j][1]-strip[i][1])>=min_d:
                        break
                  distance=calculate_distance(strip[i],strip[j])
                  if distance<min_d:
                        min_d=distance
                        closest_pair=(strip[i],strip[j])
      return min_d,closest_pair

def closest_pair_recursive(ax, points_sorted_x, points_sorted_y):
    n = len(points_sorted_x)
    if n <= 3:
        # Brute force for small datasets
        min_d = float('inf')
        closest_pair = (None, None)
        for i in range(n):
            for j in range(i + 1, n):
                distance = calculate_distance(points_sorted_x[i], points_sorted_x[j])
                if distance < min_d:
                    min_d = distance
                    closest_pair = (points_sorted_x[i], points_sorted_x[j])
        return min_d, closest_pair

    # Divide points into two halves
    mid = n // 2
    midpoint = points_sorted_x[mid]

    # Draw dividing line
    ax.axvline(x=midpoint[0], color='red', linestyle='--', alpha=0.6)
    plt.pause(0.1)

    left_x = points_sorted_x[:mid]
    right_x = points_sorted_x[mid:]
    left_y = [p for p in points_sorted_y if p[0] <= midpoint[0]]
    right_y = [p for p in points_sorted_y if p[0] > midpoint[0]]

    # Recursively find closest pairs in left and right halves
    d_left, closest_pair_left = closest_pair_recursive(ax, left_x, left_y)
    d_right, closest_pair_right = closest_pair_recursive(ax, right_x, right_y)

    # Find the smaller of the two distances
    if d_left < d_right:
        d_min = d_left
        closest_pair = closest_pair_left
    else:
        d_min = d_right
        closest_pair = closest_pair_right

    # Check for closest pair in the strip
    strip = [p for p in points_sorted_y if abs(p[0] - midpoint[0]) < d_min]
    d_strip, closest_pair_strip = closest_strip(strip, d_min)

    if d_strip < d_min:
        return d_strip, closest_pair_strip
    return d_min, closest_pair

def closest_pair(points):
    points_sorted_x = mysrt.merge_sort(points, key=lambda p: p[0])  # Sort by x-coordinate
    points_sorted_y = mysrt.merge_sort(points, key=lambda p: p[1])  # Sort by y-coordinate

    # Setup matplotlib plot
    fig, ax = plt.subplots()
    ax.scatter(*zip(*points), color='blue', label="Points")
    ax.set_title("CENG 383 Closest Pair ")
    ax.set_xlim(-50, 50)  
    ax.set_ylim(-50, 50)  

    # Find the closest pair
    min_distance, closest_pair = closest_pair_recursive(ax, points_sorted_x, points_sorted_y)

    # Highlight the closest pair
    ax.plot(
        [closest_pair[0][0], closest_pair[1][0]],
        [closest_pair[0][1], closest_pair[1][1]],
        color='green',
        linewidth=2,
        label=f"Closest Pair (Distance: {min_distance:.2f})"
    )
    ax.legend()
    plt.show()
    return min_distance, closest_pair


file_path='points_.txt'
points=read_points(file_path)
# x_points=[point[0] for point in points]
# y_points=[point[1] for point in points]
# median=stat.median(x_points)
# plt.figure(figsize=(8,8))
# plt.scatter(x_points,y_points,color='blue')
# plt.axvline(x=median,color='red', linestyle='--')
# plt.grid(True)
#plt.show()          
  
if __name__=='__main__':
    # Divide and conquer
      min_dist, closest=closest_pair(points)
      print(f"The closest pair is {closest} with a distance of {min_dist:.2f}")

    # Brute Force
    #   n=len(points)
    #   min_dist,closest_pair,steps=naive_alg(points,n)
    #   animate_algorithm(points,steps)
    #   print(naive_alg(points,n))  