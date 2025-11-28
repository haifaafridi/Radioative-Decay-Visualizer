# ☢ Radioactive Decay Visualizer (Physics Mode)

A modern **Tkinter + Matplotlib desktop application** that simulates and visualizes the radioactive decay process using **real half-life data** and the **exponential decay law**.  
This project combines **physics concepts, data structures (Linked List), probability, and GUI design** into one interactive tool.

---

## 🚀 Features

✅ Real half-life based simulation  
✅ Built-in isotopes + Custom half-life option  
✅ Balanced physics time-step: **Δt = T₁/₂ / 50**  
✅ Linked List data structure to track atom decays  
✅ Real-time visualization with Matplotlib  
✅ Modern dark-themed UI  
✅ Error handling & input validation  

---

## 🧪 Supported Isotopes

- Carbon-14  
- Uranium-238  
- Plutonium-239  
- Iodine-131  
- Cobalt-60  
- Radium-226  
- Radon-222  
- Strontium-90  
- Cesium-137  
- Tritium (H-3)  
- Polonium-210  
- **Custom (User Defined)**

---

## 🧠 Physics Behind the Simulation

This simulation uses the **exponential decay law**:

\[
P = 1 - e^{-\lambda \Delta t}
\]

Where:

- \(\lambda = \frac{\ln(2)}{T_{1/2}}\)
- \(\Delta t = \frac{T_{1/2}}{50}\)

Each atom has a random chance to decay during every time step based on this probability.

---

## 📊 What the App Shows

- **Remaining atoms**
- **Decayed atoms**
- **Decay percentage**
- A live **graph of decay vs time**
- Dynamic time scaling based on selected isotope

---

## 🏗️ Data Structures Used

The project uses a **custom Linked List** to track decayed atoms efficiently:

```python
class Node:
   atom_id
   decay_step
   next
This allows:

Fast appends

Efficient tracking

Step-wise decay analysis

🖥️ Technologies Used
Python 3

Tkinter

Matplotlib

Math / Random modules

Object-Oriented Programming

Linked Lists

📦 Installation
Install required library first:

bash
Copy code
pip install matplotlib
Then run your program:

bash
Copy code
python main.py
(Rename your python file to main.py for GitHub clarity.)

🧑‍💻 How To Use
Select an isotope from the dropdown

Enter number of atoms

Enter number of simulation steps

Click RUN SIMULATION

View graph and stats on the right

For Custom isotope, type your own half-life value.

📸 UI Preview
(Add screenshot here later)

markdown
Copy code
![App Screenshot](screenshot.png)
🧩 Project Structure
text
Copy code
radioactive-decay-simulator/
│
├── main.py
├── README.md
├── screenshot.png (optional)
✨ Future Improvements
Add 3D atom visualization

Export graph as image or PDF

Add speed control (slow/fast simulation)

Multi-isotope comparison mode

👩‍💻 Author
Haifa Afridi
Software Engineering Student @ NUST
Physics + Programming Enthusiast 💻⚛️