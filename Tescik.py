from tkinter import  *
import time

class Regulator_PID:
    def __init__(self):
        self.kp = 100
        self.ki = 0.1
        self.kd = 0
        self.calka = 0
        self.uchyb_pop = 0
        self.u = 0
    def regulacja(self, x, y, max_u, dt):
        self.uchyb = x - y
        self.wzmocnienie = self.kp * self.uchyb
        self.calka = self.ki * (self.calka + self.uchyb * dt)
        self.rozniczka = self.kd * (self.uchyb - self.uchyb_pop) / dt
        self.sterowanie = self.wzmocnienie + self.calka
        self.uchyb_pop = self.uchyb
        self.u = self.sterowanie
        if self.u < -max_u:
            self.u = -max_u
        if self.u > max_u:
            self.u = max_u
        return self.u

class Model(Regulator_PID):
    def __init__(self):
        self.m = 10
        self.g = 9.8
        self.s = 100
        self.u = 0.2
        self.v_0 = 0
        self.v = 0
        self.dt = 0.01
        self.ds = 0
        self.f_wyp = 0
        self.f_t = 0
        self.x = 200
        self.dx = 0
    def ruch(self):
        self.v_zad = Regulator_s.regulacja(self.x, self.s, 5, self.dt)
        self.f = Regulator_v.regulacja(self.v_zad, self.v, 1000, self.dt)
        if self.v >= 0:
            self.f_t = (self.m * self.g * self.u)
        if self.v < 0:
            self.f_t = -(self.m * self.g * self.u)
        self.f_wyp = float(self.f - self.f_t)
        self.a = float(self.f_wyp / self.m)
        self.ds = self.a * self.dt + self.v_0
        self.v = self.v_0 + self.a * self.dt
        self.s = self.s + self.ds
        self.v_0 = self.v
        return self.ds

class Symulacja(Model, Regulator_PID):

    def zwiekszNastaw(self, event):
        self.dx = 10
        return self.dx

    def zmniejszNastaw(self, event):
        self.dx = -10
        return self.dx

    def wyswietlanie(self, zmienna, liczba, wiersz):
        temp = str(zmienna)
        temp_int = int(liczba)
        temp_char = str(temp_int)
        self.canvas.create_text(20, 30+40*wiersz, anchor=W, font="Purisa", text=temp + temp_char)
        self.canvas.create_rectangle(10, 10+40*wiersz, 6000, 50+40*wiersz, fill="white")
        self.canvas.create_text(20, 30+40*wiersz, anchor=W, font="Purisa", text=temp + temp_char)

    def animacja(self):

        self.canvas = Canvas(tk, width=800, height=600, )
        tk.title("Tarcie")
        self.canvas.pack()
        tk.bind('<Up>', self.zwiekszNastaw)
        tk.bind('<Down>', self.zmniejszNastaw)
        self.obiekt = self.canvas.create_rectangle(50, 400, 150, 500, fill="green")
        self.podloze = self.canvas.create_rectangle(0, 500, 1500, 505, fill="black")
        self.zadana = self.canvas.create_rectangle(self.x, 490, self.x + 5, 515, fill="red")
        while TRUE:
            self.canvas.move(self.obiekt, self.ds, 0)
            self.canvas.move(self.zadana, self.dx, 0)
            self.x = self.x + self.dx
            self.dx = 0
            tk.update()
            self.ds = Sim1.ruch()
            self.wyswietlanie("zadana= ", self.x, 1)
            self.wyswietlanie("pozycja= ", self.s, 2)
            time.sleep(self.dt)

tk = Tk()
Regulator_v = Regulator_PID()
Regulator_s = Regulator_PID()
Sim1 = Symulacja()
Sim1.animacja()
tk.mainloop()
