import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import seaborn as sns

def main():
    print("=== BÀI TẬP LỚN VẬT LÝ A1 - BÀI 1 ===")
    print("Xác định quỹ đạo chuyển động của chất điểm")
    print("------------------------------------------")
    
    # 1. Nhập các giá trị ban đầu từ người dùng
    try:
        x0_val = float(input("Nhập biên độ x0 (ví dụ: 5): "))
        y0_val = float(input("Nhập biên độ y0 (ví dụ: 5): "))
        phi_deg = float(input("Nhập độ lệch pha phi bằng độ (ví dụ: 90): "))
    except ValueError:
        print("Lỗi: Định dạng dữ liệu nhập vào không hợp lệ!")
        return

    phi_rad = np.radians(phi_deg)

    # 2. Giải hệ phương trình và tìm phương trình quỹ đạo dùng Symbolic
    print("\n[1] PHƯƠNG TRÌNH CHUYỂN ĐỘNG THAM SỐ:")
    print(f" x(t) = {x0_val} * cos(5t)")
    print(f" y(t) = {y0_val} * cos(5t + {phi_deg}°)")
    
    t = sp.symbols('t', real=True)
    x, y = sp.symbols('x y', real=True)
    
    # Thiết lập và giải hệ phương trình khử t
    # Phương trình tổng quát: (x/x0)^2 + (y/y0)^2 - 2xy/(x0*y0)*cos(phi) = sin(phi)^2
    expr = x**2 / x0_val**2 + y**2 / y0_val**2 - 2*x*y / (x0_val * y0_val) * np.cos(phi_rad)
    val = np.sin(phi_rad)**2
    nice_expr = sp.nsimplify(expr, tolerance=1e-10, rational=True)
    
    print("\n[2] PHƯƠNG TRÌNH QUỸ ĐẠO SAU KHI KHỬ THAM SỐ t:")
    print(f" {nice_expr} = {val:.4g}")
    
    # Biện luận kết luận về quỹ đạo
    if np.isclose(np.sin(phi_rad), 0):
        print("\n=> KẾT LUẬN: Quỹ đạo của vật là một ĐOẠN THẲNG đi qua gốc tọa độ.")
    elif phi_deg % 180 == 90:
        if x0_val == y0_val:
            print(f"\n=> KẾT LUẬN: Quỹ đạo của vật là một ĐƯỜNG TRÒN tâm O bán kính R = {x0_val}.")
        else:
            print("\n=> KẾT LUẬN: Quỹ đạo của vật là một ĐƯỜNG ELIP CHÍNH TẮC.")
    else:
        print("\n=> KẾT LUẬN: Quỹ đạo của vật là một ĐƯỜNG ELIP BỊ XOAY (NGHIÊNG).")

    # 3. Vẽ hình quỹ đạo của vật
    print("\n[3] ĐANG VẼ ĐỒ THỊ QUỸ ĐẠO...")
    
    # Mảng thời gian t cho một chu kỳ đầy đủ T = 2*pi/5
    time_array = np.linspace(0, 2*np.pi/5, 500)
    x_t = x0_val * np.cos(5 * time_array)
    y_t = y0_val * np.cos(5 * time_array + phi_rad)
    
    # Thiết lập theme của seaborn
    sns.set_theme(style="whitegrid")
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Vẽ quỹ đạo bằng Seaborn (estimator=None để không gộp các điểm có cùng tọa độ x)
    sns.lineplot(x=x_t, y=y_t, color='#8b5cf6', linewidth=2.5, label='Quỹ đạo (Trajectory)', ax=ax, sort=False, estimator=None)
    # Vẽ điểm xuất phát bằng Seaborn
    sns.scatterplot(x=[x_t[0]], y=[y_t[0]], color='#fbcfe8', s=100, label='Điểm bắt đầu (t=0)', ax=ax, zorder=5)
    
    # Giới hạn trục tọa độ cân xứng
    max_val = max(x0_val, y0_val) * 1.2
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    
    # Đưa các trục tọa độ về gốc O(0,0)
    ax.spines['left'].set_position('zero')
    ax.spines['left'].set_color('#172554')
    ax.spines['bottom'].set_position('zero')
    ax.spines['bottom'].set_color('#172554')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.grid(color='#172554', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.set_aspect('equal', adjustable='box')
    
    ax.set_xlabel('Trục x', fontsize=9, loc='right')
    ax.set_ylabel('Trục y', fontsize=9, loc='top')
    ax.legend(loc='upper right', framealpha=0.8, fontsize=8)
    
    plt.title(f"Quỹ đạo chuyển động của chất điểm\n(x0={x0_val}, y0={y0_val}, phi={phi_deg}°)", fontsize=11)
    plt.show()

if __name__ == '__main__':
    main()
