"""
This is where you should write your code and this is what you need to upload to Gradescope for autograding.

You must NOT change the function definitions (names, arguments).

You can run the functions you define in this file by using test.py (python test.py)
Please do not add any additional code underneath these functions.
"""

import sqlite3
conn = sqlite3.connect("tickets.db")

def customer_tickets(conn, customer_id):
    """
    Return a list of tuples:
    (film_title, screen, price)

    Include only tickets purchased by the given customer_id.
    Order results by film title alphabetically.
    """
    

    q = """SELECT f.title, s.screen, t.price
    FROM films f JOIN screenings s ON f.film_id=s.film_id
    JOIN tickets t ON t.screening_id=s.screening_id
    WHERE t.customer_id=?
    ORDER BY f.title;"""

    cur = conn.execute(q, (customer_id,))

    return cur.fetchall()
    


def screening_sales(conn):
    """
    Return a list of tuples:
    (screening_id, film_title, tickets_sold)

    Include all screenings, even if tickets_sold is 0.
    Order results by tickets_sold descending.
    """

    q = """SELECT s.screening_id, f.title, COUNT(t.ticket_id) AS t_sold
    FROM screenings s LEFT JOIN tickets t ON s.screening_id=t.screening_id
    JOIN films f ON f.film_id=s.film_id
    GROUP BY s.screening_id
    ORDER BY t_sold DESC;"""

    cur = conn.execute(q)
    return cur.fetchall()
    




def top_customers_by_spend(conn, limit):
    """
    Return a list of tuples:
    (customer_name, total_spent)

    total_spent is the sum of ticket prices per customer.
    Only include customers who have bought at least one ticket.
    Order by total_spent descending.
    Limit the number of rows returned to `limit`.
    """
    
    q = """SELECT c.customer_name, SUM(t.price) AS spent
    FROM customers c LEFT JOIN tickets t ON c.customer_id=t.customer_id
    GROUP BY c.customer_id HAVING COUNT(t.ticket_id) >= 1
    ORDER BY spent DESC
    LIMIT ?;
    """

    cur = conn.execute(q, (limit,))
    return cur.fetchall()