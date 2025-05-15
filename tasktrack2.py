pip install -r requirements.txt
import streamlit as st
from datetime import datetime
import pandas as pd

# Class untuk Tugas
class Task:
    def __init__(self, title, deadline, description, priority, subject):
        self.title = title
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        self.description = description
        self.priority = priority
        self.subject = subject
        self.status = "Belum Selesai"

    def mark_as_done(self):
        self.status = "Selesai"

    def remind(self):
        now = datetime.now()
        time_diff = self.deadline - now
        days_left = time_diff.days
        if days_left > 0:
            return f"🔔 '{self.title}' tinggal {days_left} hari lagi!"
        elif days_left == 0:
            return f"⚡ Deadline '{self.title}' adalah hari ini!"
        else:
            return f"❗ '{self.title}' sudah lewat deadline!"

    def auto_cluster_priority(self):
        now = datetime.now()
        days_left = (self.deadline - now).days
        if days_left <= 3:
            return "Tinggi"
        elif 4 <= days_left <= 7:
            return "Sedang"
        else:
            return "Rendah"

# Manajemen Tugas
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, title):
        self.tasks = [t for t in self.tasks if t.title != title]

    def complete_task(self, title):
        for t in self.tasks:
            if t.title == title:
                t.mark_as_done()

    def get_tasks(self):
        return self.tasks

# Inisialisasi TaskManager
if "manager" not in st.session_state:
    st.session_state.manager = TaskManager()

st.title("📋 TaskTrack - Pengingat & Manajemen Tugas")

# Ganti dari selectbox menjadi radio (sidebar menu)
menu = st.sidebar.radio("📌 Navigasi", [
    "Tambah Tugas", 
    "Lihat Semua Tugas", 
    "Tugas Belum Selesai", 
    "Reminder", 
    "Urutkan Deadline", 
    "Hapus Tugas", 
    "Tandai Selesai"
])

# Tambah Tugas
if menu == "Tambah Tugas":
    st.subheader("➕ Tambah Tugas Baru")
    title = st.text_input("Nama Tugas")
    deadline = st.text_input("Deadline (YYYY-MM-DD HH:MM)")
    description = st.text_area("Deskripsi Tugas")
    priority = st.selectbox("Prioritas Manual", ["Tinggi", "Sedang", "Rendah"])
    subject = st.text_input("Mata Kuliah")

    if st.button("Simpan Tugas"):
        try:
            task = Task(title, deadline, description, priority, subject)
            st.session_state.manager.add_task(task)
            st.success(f"Tugas '{title}' berhasil ditambahkan!")
        except Exception as e:
            st.error(f"Format deadline salah. Gunakan 'YYYY-MM-DD HH:MM'.\n{e}")

# Lihat Semua Tugas
elif menu == "Lihat Semua Tugas":
    st.subheader("📚 Semua Tugas")
    tasks = st.session_state.manager.get_tasks()
    if not tasks:
        st.info("Belum ada tugas.")
    for t in tasks:
        cluster = t.auto_cluster_priority()
        st.write(f"📌 **{t.title}** - `{t.status}`")
        st.caption(f"🧠 Mata Kuliah: {t.subject} | ⏳ Deadline: {t.deadline.strftime('%Y-%m-%d %H:%M')} | 🚦 Prioritas Manual: {t.priority} | 📊 Cluster: {cluster}")
        st.markdown("---")

# Reminder
elif menu == "Reminder":
    st.subheader("🔔 Notifikasi Reminder")
    tasks = st.session_state.manager.get_tasks()
    if not tasks:
        st.info("Tidak ada tugas.")
    for t in tasks:
        st.write(t.remind())

# Urutan Deadline
elif menu == "Urutkan Deadline":
    st.subheader("📅 Urutan Tugas Berdasarkan Deadline")
    tasks = sorted(st.session_state.manager.get_tasks(), key=lambda t: t.deadline)
    for t in tasks:
        st.write(f"🗂️ {t.title} - Deadline: {t.deadline.strftime('%Y-%m-%d %H:%M')} - `{t.status}`")

# Tugas Belum Selesai
elif menu == "Tugas Belum Selesai":
    st.subheader("🚧 Tugas Belum Selesai")
    tasks = [t for t in st.session_state.manager.get_tasks() if t.status == "Belum Selesai"]
    if tasks:
        for t in tasks:
            st.write(f"- {t.title} (Deadline: {t.deadline.strftime('%Y-%m-%d %H:%M')})")
    else:
        st.success("🎉 Semua tugas sudah selesai!")

# Tandai Selesai
elif menu == "Tandai Selesai":
    st.subheader("✅ Tandai Tugas Selesai")
    titles = [t.title for t in st.session_state.manager.get_tasks() if t.status != "Selesai"]
    if titles:
        selected = st.selectbox("Pilih tugas yang ingin ditandai selesai:", titles)
        if st.button("Tandai Selesai"):
            st.session_state.manager.complete_task(selected)
            st.success(f"Tugas '{selected}' ditandai sebagai Selesai.")
    else:
        st.info("Tidak ada tugas yang belum selesai.")

# Hapus Tugas
elif menu == "Hapus Tugas":
    st.subheader("🗑️ Hapus Tugas")
    titles = [t.title for t in st.session_state.manager.get_tasks()]
    if titles:
        selected = st.selectbox("Pilih tugas yang ingin dihapus:", titles)
        if st.button("Hapus"):
            st.session_state.manager.delete_task(selected)
            st.warning(f"Tugas '{selected}' berhasil dihapus.")
    else:
        st.info("Tidak ada tugas untuk dihapus.")
