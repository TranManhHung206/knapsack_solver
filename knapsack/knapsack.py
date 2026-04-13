import os
import csv
import time
from ortools.algorithms.python import knapsack_solver

# Mỗi nhóm có 6 testcase n50 đến n2000
# Tất cả các testcase đều nằm trong mục R01000 để đánh giá công bằng hơn

# Hàm đọc dữ liệu từ file .kp có sẵn trong mục Testcases
def read_kp_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()   
    # Xóa các dòng trống và khoảng trắng thừa
    lines = [line.strip() for line in lines if line.strip()]
    
    # Dòng 1 là số lượng đồ vật (n)
    n = int(lines[0])
    # Dòng 2 là sức chứa của balo (capacity)
    capacity = int(lines[1])
    
    values = []
    weights = []
    
    # Từ dòng 3 trở đi là các cặp (value, weight)
    for i in range(2, 2 + n):
        parts = lines[i].split()
        values.append(int(parts[0]))
        weights.append(int(parts[1]))
        
    # OR-Tools yêu cầu weights là mảng 2 chiều và capacities là mảng 1 chiều
    return values, [weights], [capacity]

# Hàm giải 1 testcase
def solve_single_testcase(filepath, time_limit_seconds=180.0):
    values, weights, capacities = read_kp_file(filepath)
    
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackTest"
    )
    
    # Cài đặt thời gian tối đa cho mỗi lần chạy
    solver.set_time_limit(time_limit_seconds)
    solver.init(values, weights, capacities)
    
    # Chạy solver và tính thời gian
    time_start = time.time()
    computed_value = solver.solve()
    time_end = time.time()

    # kiểm tra kết quả tối ưu và tính thời gian
    is_optimal = solver.is_solution_optimal()
    solve_time = time_end - time_start 
    
    packed_items = []
    packed_weights = []
    total_weight = 0
    
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
            
    return computed_value, total_weight, is_optimal, packed_items, packed_weights, solve_time

def main():
    # Tên thư mục chứa các file .kp vừa copy
    test_cases_dir = "Testcases"
    output_csv = "Output_Knapsack.csv"
    time_limit = 180.0 # Giới hạn 3 phút giải testcase

    # Mở file CSV để ghi kết quả
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Ghi dòng tiêu đề
        writer.writerow(["File Name", "Solver Value", "Total Weight", "Is optimal"])

        # Lấy danh sách các file .kp và sắp xếp theo tên cho đẹp
        files = [f for f in os.listdir(test_cases_dir) if f.endswith(".kp")]
        files.sort()

        for filename in files:
            filepath = os.path.join(test_cases_dir, filename)
            print(f"Solving {filename}...", end="\n")
            
            try:
                val, weight, is_opt, p_items, p_weights, solve_time = solve_single_testcase(filepath, time_limit)
                
                # In ra kết quả
                print(f"Time taken: {solve_time:.5f} seconds")
                print("Total value =", val)
                print("Total weight:", weight)
                # print("Packed items:", p_items)
                # print("Packed weights:", p_weights)
                print("Optimal:", is_opt)
                print("\n")
                
                # Ghi kết quả vào file CSV
                opt_str = "Yes" if is_opt else "No (Time limit)"
                writer.writerow([filename, val, weight, opt_str])
                file.flush() # ghi kết quả sau khi chạy xong

            except Exception as e:
                print(f"Error: {e}")
                writer.writerow([filename, "X", "X", "X"])
                file.flush()

            time.sleep(0.5)
    print(f"All testcases solved. Solutions saved in: {output_csv}")

if __name__ == "__main__":
    main()