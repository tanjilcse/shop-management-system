import tkinter as tk
from tkinter import messagebox
from functions import *

root = tk.Tk()
root.geometry("950x650")
root.title("SHOP POS SYSTEM")

BG = "#2c3e50"
BTN = "#1abc9c"
root.config(bg=BG)

cart = []

# ---------- STYLE ----------
def clear():
    for w in root.winfo_children():
        w.destroy()

def title(t):
    return tk.Label(root, text=t, font=("Segoe UI", 20, "bold"), bg=BG, fg="white")

def btn(t, cmd):
    return tk.Button(root, text=t, command=cmd, bg=BTN, fg="white", width=22, height=2)

# ---------- START ----------
def start():
    clear()
    title("SHOP MANAGEMENT SYSTEM").pack(pady=30)

    btn("ADMIN LOGIN", login_ui).pack(pady=10)
    btn("CUSTOMER", customer_ui).pack(pady=10)
    btn("EXIT", root.quit).pack(pady=10)

# ---------- LOGIN ----------
def login_ui():
    clear()
    title("ADMIN LOGIN").pack()

    tk.Label(root, text="Username", bg=BG, fg="white").pack()
    u = tk.Entry(root)
    u.pack()

    tk.Label(root, text="Password", bg=BG, fg="white").pack()
    p = tk.Entry(root, show="*")
    p.pack()

    def login():
        if admin_login(u.get(), p.get()):
            admin()
        else:
            messagebox.showerror("Error", "Wrong login")

    btn("LOGIN", login).pack()
    btn("BACK", start).pack()

# ---------- ADMIN ----------
def admin():
    clear()
    title("ADMIN DASHBOARD").pack(pady=20)

    btn("ADD PRODUCT", add_ui).pack(pady=5)
    btn("SEARCH / VIEW", view_ui).pack(pady=5)
    btn("UPDATE PRODUCT", update_ui).pack(pady=5)
    btn("DELETE PRODUCT", delete_ui).pack(pady=5)
    btn("PROFIT REPORT", profit_ui).pack(pady=5)
    btn("LOGOUT", start).pack(pady=10)

# ---------- ADD ----------
def add_ui():
    clear()
    title("ADD PRODUCT").pack()

    e = [tk.Entry(root) for _ in range(5)]
    labels = ["Name", "Price", "Cost", "Qty", "Category"]

    for i in range(5):
        tk.Label(root, text=labels[i], bg=BG, fg="white").pack()
        e[i].pack()

    def add():
        add_product(
            e[0].get(),
            float(e[1].get()),
            float(e[2].get()),
            int(e[3].get()),
            e[4].get()
        )
        messagebox.showinfo("OK", "Added")

    btn("ADD", add).pack()
    btn("BACK", admin).pack()

# ---------- VIEW ----------
def view_ui():
    clear()
    title("SEARCH / VIEW").pack()

    tk.Label(root, text="Search Name", bg=BG, fg="white").pack()
    s = tk.Entry(root)
    s.pack()

    tk.Label(root, text="Category", bg=BG, fg="white").pack()
    c = tk.Entry(root)
    c.pack()

    out = tk.Text(root, width=90, height=20)
    out.pack()

    def load():
        out.delete(1.0, tk.END)
        for d in get_products(s.get(), c.get()):
            warn = "⚠ LOW STOCK" if d['quantity'] < 5 else ""
            out.insert(tk.END, f"{d['name']} | {d['price']} | {d['quantity']} {warn}\n")

    btn("SEARCH", load).pack()
    btn("BACK", admin).pack()

    load()

# ---------- UPDATE ----------
def update_ui():
    clear()
    title("UPDATE PRODUCT").pack()

    tk.Label(root, text="Product Name", bg=BG, fg="white").pack()
    n = tk.Entry(root)
    n.pack()

    tk.Label(root, text="New Price", bg=BG, fg="white").pack()
    p = tk.Entry(root)
    p.pack()

    tk.Label(root, text="Category", bg=BG, fg="white").pack()
    c = tk.Entry(root)
    c.pack()

    def update():
        update_product(n.get(), float(p.get()), c.get())
        messagebox.showinfo("Success", "Updated")

    btn("UPDATE", update).pack()
    btn("BACK", admin).pack()

# ---------- DELETE ----------
def delete_ui():
    clear()
    title("DELETE PRODUCT").pack()

    tk.Label(root, text="Product Name", bg=BG, fg="white").pack()
    n = tk.Entry(root)
    n.pack()

    def delete():
        delete_product(n.get())
        messagebox.showinfo("Deleted", "Removed")

    btn("DELETE", delete).pack()
    btn("BACK", admin).pack()

# ---------- PROFIT ----------
def profit_ui():
    clear()
    title("PROFIT REPORT").pack()

    total, daily, weekly, monthly = profit_report()

    tk.Label(root, text=f"TOTAL: {total}", bg=BG, fg="green").pack()

    out = tk.Text(root, width=90, height=25)
    out.pack()

    out.insert(tk.END, "DAILY\n")
    for d in daily:
        out.insert(tk.END, f"{d['day']} → {d['total']}\n")

    out.insert(tk.END, "\nWEEKLY\n")
    for w in weekly:
        out.insert(tk.END, f"{w['week']} → {w['total']}\n")

    out.insert(tk.END, "\nMONTHLY\n")
    for m in monthly:
        out.insert(tk.END, f"{m['month']} → {m['total']}\n")

    btn("BACK", admin).pack()

# ---------- CUSTOMER ----------
def customer_ui():
    clear()
    title("CUSTOMER PANEL").pack()

    btn("VIEW PRODUCTS", customer_view_ui).pack()
    btn("BUY PRODUCT", buy_ui).pack()
    btn("BACK", start).pack()

# ---------- NEW VIEW PRODUCT ----------
def customer_view_ui():
    clear()
    title("PRODUCT LIST").pack()

    tk.Label(root, text="Search Name", bg=BG, fg="white").pack()
    s = tk.Entry(root)
    s.pack()

    tk.Label(root, text="Category", bg=BG, fg="white").pack()
    c = tk.Entry(root)
    c.pack()

    out = tk.Text(root, width=90, height=25)
    out.pack()

    def load():
        out.delete(1.0, tk.END)
        data = get_products(s.get(), c.get())

        if not data:
            out.insert(tk.END, "No products found\n")
            return

        for d in data:
            status = "In Stock" if d['quantity'] > 0 else "Out of Stock"
            out.insert(
                tk.END,
                f"{d['name']} | Price: {d['price']} | Qty: {d['quantity']} | {status}\n"
            )

    btn("SEARCH", load).pack()
    btn("BACK", customer_ui).pack()

    load()

# ---------- BUY ----------
def buy_ui():
    clear()
    title("BUY SYSTEM").pack(pady=15)

    main = tk.Frame(root, bg=BG)
    main.pack(pady=10)

    form = tk.Frame(main, bg=BG)
    form.grid(row=0, column=0, padx=40)

    # ---------- PRODUCT NAME ----------
    tk.Label(form, text="Product Name", bg=BG, fg="white").grid(row=0, column=0, sticky="w")
    n = tk.Entry(form, width=30)
    n.grid(row=0, column=1, pady=5)

    data = get_products()
    product_names = [i['name'] for i in data]

    listbox = tk.Listbox(form, height=5)
    listbox.grid(row=1, column=1, sticky="we")
    listbox.grid_remove()

    def update_suggestions(event):
        typed = n.get().lower()
        listbox.delete(0, tk.END)

        if typed == "":
            listbox.grid_remove()
            return

        matches = [name for name in product_names if typed in name.lower()]

        if matches:
            for name in matches:
                listbox.insert(tk.END, name)
            listbox.grid()
        else:
            listbox.grid_remove()

    n.bind("<KeyRelease>", update_suggestions)

    def select_item(event):
        if listbox.curselection():
            selected = listbox.get(listbox.curselection())
            n.delete(0, tk.END)
            n.insert(0, selected)
            listbox.grid_remove()

    listbox.bind("<<ListboxSelect>>", select_item)

    # ---------- OTHER FIELDS ----------
    tk.Label(form, text="Quantity", bg=BG, fg="white").grid(row=2, column=0, sticky="w")
    q = tk.Entry(form, width=30)
    q.grid(row=2, column=1, pady=5)

    tk.Label(form, text="Customer Name", bg=BG, fg="white").grid(row=3, column=0, sticky="w")
    cust = tk.Entry(form, width=30)
    cust.grid(row=3, column=1, pady=5)

    tk.Label(form, text="Phone", bg=BG, fg="white").grid(row=4, column=0, sticky="w")
    ph = tk.Entry(form, width=30)
    ph.grid(row=4, column=1, pady=5)

    tk.Label(form, text="Payment Method", bg=BG, fg="white").grid(row=5, column=0, sticky="w")
    pay = tk.StringVar()
    pay.set("Cash")
    tk.OptionMenu(form, pay, "Cash", "Mobile", "Due").grid(row=5, column=1, pady=5, sticky="we")

    tk.Label(form, text="Paid Amount (for Due)", bg=BG, fg="white").grid(row=6, column=0, sticky="w")
    paid_entry = tk.Entry(form, width=30)
    paid_entry.grid(row=6, column=1, pady=5)

    # ---------- CART ----------
    cart_frame = tk.Frame(main, bg=BG)
    cart_frame.grid(row=0, column=1)

    tk.Label(cart_frame, text="CART", font=("Segoe UI", 14, "bold"), bg=BG, fg="white").pack()

    cart_box = tk.Text(cart_frame, height=15, width=45)
    cart_box.pack(pady=10)

    def refresh():
        cart_box.delete(1.0, tk.END)
        for i in cart:
            cart_box.insert(tk.END, f"{i[0]} | Qty: {i[1]} | Total: {i[2]}\n")

    # ---------- ADD CART ----------
    def add_cart():
        data = get_products()
        p = next((i for i in data if i['name'] == n.get()), None)

        if not p:
            messagebox.showerror("Error", "Product not found")
            return

        qty = int(q.get())

        if qty > p['quantity']:
            messagebox.showerror("Error", "Not enough stock")
            return

        total_price = float(p['price']) * qty

        for i in range(len(cart)):
            if cart[i][0] == n.get():
                old = cart[i][1]
                cart[i] = (n.get(), old + qty, float(p['price']) * (old + qty))
                break
        else:
            cart.append((n.get(), qty, total_price))

        refresh()
        messagebox.showinfo("OK", "Added")

    # ---------- CHECKOUT ----------
    def checkout():
        try:
            if not cart:
                messagebox.showerror("Error", "Cart is empty")
                return

            subtotal = sum(float(i[2]) for i in cart)
            discount = subtotal * 0.10 if len(cart) >= 5 else 0.0
            vat = subtotal * 0.05
            total = subtotal + vat - discount

            customer_name = cust.get()
            phone = ph.get()

            if customer_name == "" or phone == "":
                messagebox.showerror("Error", "Customer info required")
                return

            method = pay.get()

            if method in ["Cash", "Mobile"]:
                paid = total
                due = 0
            else:
                if paid_entry.get() == "":
                    messagebox.showerror("Error", "Enter paid amount")
                    return
                paid = float(paid_entry.get())
                due = total - paid

            # Record Sale and Update Stock
            for i in cart:
                record_sale(i[0], i[1], float(i[2]), customer_name, phone, method, paid, due)
                update_stock(i[0], i[1])

            # Create Bill Text
            bill = "🧾 ===== INVOICE =====\n\n"
            bill += f"Customer: {customer_name}\nPhone: {phone}\n"
            bill += f"Payment: {method}\nPaid: {paid}\nDue: {due}\n\n"

            for i in cart:
                bill += f"{i[0]} | Qty:{i[1]} | Total:{i[2]}\n"

            bill += f"\nSubtotal: {subtotal:.2f}\nDiscount: {discount:.2f}\nVAT: {vat:.2f}\nTOTAL: {total:.2f}"

            with open("receipt.txt", "w", encoding="utf-8") as f:
                f.write(bill)

            cart.clear()
            refresh()
            messagebox.showinfo("SUCCESS", bill)

        except Exception as e:
            messagebox.showerror("ERROR", str(e))

    # ---------- BUTTONS ----------
    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.pack(pady=15)

    btn("ADD TO CART", add_cart).pack(pady=5)
    btn("CHECKOUT", checkout).pack(pady=5)
    btn("BACK", customer_ui).pack(pady=5)

# ---------- RUN ----------
start()
root.mainloop()