from db_config import get_connection

# ---------- LOGIN ----------
def admin_login(u,p):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT * FROM admins WHERE username=%s AND password=%s",(u,p))
    r=cur.fetchone()
    conn.close()
    return r

# ---------- PRODUCT ----------
def add_product(n,sp,cp,q,c):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""
    INSERT INTO inventory(name,price,cost_price,quantity,category)
    VALUES(%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE quantity=quantity+%s
    """,(n,sp,cp,q,c,q))
    conn.commit()
    conn.close()

def get_products(name="",cat=""):
    conn=get_connection()
    cur=conn.cursor(dictionary=True)

    q="SELECT * FROM inventory WHERE 1=1"
    v=[]

    if name:
        q+=" AND name LIKE %s"
        v.append(f"%{name}%")

    if cat:
        q+=" AND category=%s"
        v.append(cat)

    cur.execute(q,v)
    d=cur.fetchall()
    conn.close()
    return d

def update_product(n,sp,c):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("UPDATE inventory SET price=%s,category=%s WHERE name=%s",(sp,c,n))
    conn.commit()
    conn.close()

def delete_product(n):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM inventory WHERE name=%s",(n,))
    conn.commit()
    conn.close()

def update_stock(n,q):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("UPDATE inventory SET quantity=quantity-%s WHERE name=%s",(q,n))
    conn.commit()
    conn.close()

# ---------- SALES ----------
def record_sale(n, q, t, cust, ph, method, paid, due):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO sales(
        product_name,
        quantity_sold,
        total_price,
        customer_name,
        phone,
        payment_method,
        paid_amount,
        due_amount
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """, (n, q, t, cust, ph, method, paid, due))

    conn.commit()
    conn.close()

# ---------- PROFIT ----------
def profit_report():
    conn=get_connection()
    cur=conn.cursor(dictionary=True)

    cur.execute("SELECT SUM(total_price) total FROM sales")
    total=cur.fetchone()['total']

    cur.execute("""
        SELECT DATE(sale_date) day,SUM(total_price) total
        FROM sales GROUP BY DATE(sale_date)
    """)
    daily=cur.fetchall()

    cur.execute("""
        SELECT YEARWEEK(sale_date) week,SUM(total_price) total
        FROM sales GROUP BY YEARWEEK(sale_date)
    """)
    weekly=cur.fetchall()

    cur.execute("""
        SELECT DATE_FORMAT(sale_date,'%Y-%m') month,SUM(total_price) total
        FROM sales GROUP BY month
    """)
    monthly=cur.fetchall()

    conn.close()
    return total,daily,weekly,monthly