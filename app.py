import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import calendar
import locale

st.set_page_config(page_title="APLIKASI PROGRAM ATLET", page_icon=":runner:", layout="wide")

st.markdown("""
<style>
    .main {
        padding: 0.25rem;
        max-width: 800px;
        margin: 0 auto;
    }
    @media (max-width: 768px) {
        .main {
            padding: 0.1rem;
        }
        .stButton>button {
            font-size: 0.8em;
            padding: 0.2rem;
        }
        h1 {
            font-size: 1.2em;
        }
        h2 {
            font-size: 1em;
        }
        .calendar-day {
            font-size: 0.7em;
            padding: 2px;
            min-height: 20px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            transform: rotate(0deg);
            writing-mode: horizontal-tb;
            border: 1px solid #999;
            background-color: transparent;
            color: #333;
        }
        .calendar-day-program {
            font-size: 0.65em;
            padding: 2px;
            border-radius: 3px;
            margin: 1px 0;
        }
        .st-emotion-cache-1r6slb0 {
            gap: 0.1rem !important;
        }
    }
    .stButton>button {
        width: 100%;
        margin: 0.3rem 0;
    }
    h1, h2 {
        margin: 0.5rem 0;
        font-size: 1.3em;
    }
    .calendar-day {
        padding: 2px;
        margin: 0;
        text-align: center;
        font-size: 0.8em;
        min-height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #999;
        background-color: #E6F3FF;
        color: #333;
    }
    .calendar-day-program {
        background-color: #e7f3ff;
        padding: 2px;
        margin: 0;
        text-align: center;
        border-radius: 2px;
        font-weight: 500;
        font-size: 0.75em;
        color: #0066cc;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 1px 1px rgba(0,102,204,0.1);
    }
    .calendar-day-program:hover {
        background-color: #d1e9ff;
        box-shadow: 0 1px 2px rgba(0,102,204,0.15);
    }
</style>
""", unsafe_allow_html=True)

import json
import hashlib

# Fungsi untuk membaca data pengguna
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

# Fungsi untuk hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# State untuk login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

# Fungsi untuk menyimpan pengguna baru
def save_user(username, password, role, name, phone):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        'password': hash_password(password),
        'role': role,
        'name': name,
        'phone': phone
    }
    with open('users.json', 'w') as f:
        json.dump(users, f)
    return True



# Nama bulan dan hari dalam bahasa Indonesia
month_names = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
day_names = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']

# Fungsi untuk membuat kalender
def create_calendar(year, month, programs_data):
    cal = calendar.monthcalendar(year, month)
    month_name = month_names[month]
    
    # Buat header kalender dengan kolom kosong
    cols = st.columns(7)
    
    # Isi kalender dengan program
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day != 0:
                date_str = f"{year}-{month:02d}-{day:02d}"
                if date_str in programs_data:
                    progs = programs_data[date_str]
                    with cols[i]:
                        st.markdown("""
                        <style>
                        [data-testid="column"]:has(div.has-program) {
                            background-color: #0066cc;
                            border-radius: 5px;
                            padding: 5px;
                            margin: 2px;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        st.markdown("<div class='has-program'>", unsafe_allow_html=True)
                        st.markdown(f"<div class='calendar-day' style='text-align: center; color: #0066cc; font-size: 1.1em; font-weight: bold;'>{day_names[i]} {day}</div>", unsafe_allow_html=True)
                        for prog in progs:
                            with st.expander(prog['name']):
                                st.write(f"Deskripsi: {prog['description']}")
                                st.write(f"Durasi: {prog['duration']} jam")
                                st.write(f"Intensitas: {prog['intensity']}")
                                st.write(f"Coach: {prog['coach']}")
                                
                                # Tambahkan status program dan tombol selesai
                                program_status = prog.get('status', 'Belum Selesai')
                                st.write(f"Status: {program_status}")
                                
                                if program_status == 'Belum Selesai':
                                    if st.button('Tandai Selesai', key=f"complete_{date_str}_{prog['name']}_calendar"):
                                        prog['status'] = 'Menunggu Evaluasi'
                                        with open('assigned_programs.json', 'w') as f:
                                            json.dump(assigned_programs, f)
                                        st.success('Program ditandai sebagai selesai!')
                                        st.rerun()
                                
                                # Tampilkan evaluasi jika ada
                                if 'evaluation' in prog:
                                    st.write(f"Evaluasi Pelatih: {prog['evaluation']}")
                        st.markdown("</div>", unsafe_allow_html=True)

                else:
                    with cols[i]:
                        st.markdown(f"<div class='calendar-day' style='text-align: center; color: #999; background-color: transparent;'>{day_names[i]} {day}</div>", unsafe_allow_html=True)
                        with st.expander("Tidak ada program"):
                            st.write("Tidak ada program pada tanggal ini.")

# Tampilkan tombol logout di bagian atas jika sudah login
if st.session_state.logged_in:
    col1, col2 = st.columns([10,1])
    with col2:
        if st.button('Logout', key='logout_button_top'):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()

# Tampilkan halaman login dan registrasi jika belum login
if not st.session_state.logged_in:
    st.title('APLIKASI PROGRAM ATLET :runner:')
    tab1, tab2 = st.tabs(['Login', 'Registrasi'])
    
    with tab1:
        st.header('Login')
        username = st.text_input('Username', key='login_username')
        password = st.text_input('Password', type='password', key='login_password')
        
        if st.button('Login'):
            users = load_users()
            if username in users and users[username]['password'] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = users[username]['role']
                st.rerun()
            else:
                st.error('Username atau password salah')
    
    with tab2:
        st.header('Registrasi')
        new_username = st.text_input('Username', key='reg_username')
        new_password = st.text_input('Password', type='password', key='reg_password')
        confirm_password = st.text_input('Konfirmasi Password', type='password')
        role = st.selectbox('Role', ['athlete', 'coach'])
        name = st.text_input('Nama Lengkap')
        phone = st.text_input('Nomor Telepon')
        
        if st.button('Daftar'):
            if new_password != confirm_password:
                st.error('Password tidak cocok')
            elif not new_username or not new_password or not name or not phone:
                st.error('Semua field harus diisi')
            else:
                if save_user(new_username, new_password, role, name, phone):
                    st.success('Registrasi berhasil! Silakan login.')
                else:
                    st.error('Username sudah digunakan')
else:
    if st.session_state.role == 'coach':
        st.title('Dashboard Pelatih')
        st.write(f'Selamat datang, {st.session_state.username}!')
        
        # Tampilkan dan edit profil pelatih
        st.header('Profil Pelatih')
        users = load_users()
        user_data = users[st.session_state.username]
        
        with st.expander('Edit Profil'):
            new_name = st.text_input('Nama Lengkap', value=user_data.get('name', ''))
            new_phone = st.text_input('Nomor Telepon', value=user_data.get('phone', ''))
            new_password = st.text_input('Password Baru (kosongkan jika tidak ingin mengubah)', type='password')
            
            if st.button('Simpan Perubahan'):
                users[st.session_state.username]['name'] = new_name
                users[st.session_state.username]['phone'] = new_phone
                if new_password:
                    users[st.session_state.username]['password'] = hash_password(new_password)
                
                with open('users.json', 'w') as f:
                    json.dump(users, f)
                st.success('Profil berhasil diperbarui!')
        
        st.header('Program Latihan')
    elif st.session_state.role == 'athlete':
        st.title('Dashboard Atlet')
        st.write(f'Selamat datang, {st.session_state.username}!')
    
    # Load program data
    def load_programs():
        try:
            with open('programs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def load_assigned_programs():
        try:
            with open('assigned_programs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    programs = load_programs()
    assigned_programs = load_assigned_programs()

    # Tampilkan program berdasarkan role
    if st.session_state.role == 'coach':
        st.header('Program yang Dibuat')
        for date, progs in programs.items():
            st.subheader(f'Tanggal: {date}')
            for i, prog in enumerate(progs):
                with st.expander(f"{prog['name']} - {prog['intensity']}"):
                    if 'edit_mode' not in st.session_state:
                        st.session_state.edit_mode = {}
                    
                    edit_key = f"{date}_{i}"
                    if edit_key not in st.session_state.edit_mode:
                        st.session_state.edit_mode[edit_key] = False
                    
                    if not st.session_state.edit_mode[edit_key]:
                        st.write(f"Deskripsi: {prog['description']}")
                        st.write(f"Durasi: {prog['duration']} jam")
                        st.write(f"Intensitas: {prog['intensity']}")
                        st.write(f"Coach: {prog['coach']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button('Edit Program', key=f'edit_{edit_key}'):
                                st.session_state.edit_mode[edit_key] = True
                                st.rerun()
                        with col2:
                            if st.button('Hapus Program', key=f'delete_{edit_key}'):
                                # Hapus program dari programs.json
                                programs[date].pop(i)
                                if not programs[date]:
                                    del programs[date]
                                with open('programs.json', 'w') as f:
                                    json.dump(programs, f)
                                
                                # Hapus program dari assigned_programs.json
                                for athlete in assigned_programs:
                                    if date in assigned_programs[athlete]:
                                        if len(assigned_programs[athlete][date]) > i:
                                            assigned_programs[athlete][date].pop(i)
                                        if not assigned_programs[athlete][date]:
                                            del assigned_programs[athlete][date]
                                with open('assigned_programs.json', 'w') as f:
                                    json.dump(assigned_programs, f)
                                
                                st.success('Program berhasil dihapus!')
                                st.rerun()
                    else:
                        with st.form(f'edit_program_{edit_key}'):
                            new_name = st.text_input('Nama Program', value=prog['name'])
                            new_description = st.text_area('Deskripsi', value=prog['description'])
                            new_duration = st.number_input('Durasi (jam)', min_value=1, value=prog['duration'])
                            new_intensity = st.selectbox('Intensitas', ['Rendah', 'Sedang', 'Tinggi'], index=['Rendah', 'Sedang', 'Tinggi'].index(prog['intensity']))
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button('Simpan'):
                                    prog['name'] = new_name
                                    prog['description'] = new_description
                                    prog['duration'] = new_duration
                                    prog['intensity'] = new_intensity
                                    with open('programs.json', 'w') as f:
                                        json.dump(programs, f)
                                    st.session_state.edit_mode[edit_key] = False
                                    st.success('Program berhasil diperbarui!')
                                    st.rerun()
                            with col2:
                                if st.form_submit_button('Batal'):
                                    st.session_state.edit_mode[edit_key] = False
                                    st.rerun()

        # Pilihan penerima program
        st.header('Buat Program Baru')
        users = load_users()
        athletes = [username for username, data in users.items() if data['role'] == 'athlete']
        
        if 'recipient_type' not in st.session_state:
            st.session_state.recipient_type = 'Semua Atlet'
        if 'selected_athlete' not in st.session_state:
            st.session_state.selected_athlete = athletes[0] if athletes else None
            
        st.session_state.recipient_type = st.radio('Kirim Program Kepada:', ['Semua Atlet', 'Atlet Tertentu'])
        
        if st.session_state.recipient_type == 'Atlet Tertentu':
            st.session_state.selected_athlete = st.selectbox('Pilih Atlet', athletes)
            selected_athletes = [st.session_state.selected_athlete]
        else:
            selected_athletes = athletes
            
        # Form untuk membuat program baru
        with st.form('create_program'):
            date = st.date_input('Tanggal Program')
            name = st.text_input('Nama Program')
            description = st.text_area('Deskripsi')
            duration = st.number_input('Durasi (jam)', min_value=1, value=1)
            intensity = st.selectbox('Intensitas', ['Rendah', 'Sedang', 'Tinggi'])
            
            submit = st.form_submit_button('Buat Program')

            if submit:
                date_str = date.strftime('%Y-%m-%d')
                new_program = {
                    'name': name,
                    'description': description,
                    'duration': duration,
                    'intensity': intensity,
                    'coach': st.session_state.username,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                if date_str not in programs:
                    programs[date_str] = []
                programs[date_str].append(new_program)

                with open('programs.json', 'w') as f:
                    json.dump(programs, f)
                
                # Menugaskan program ke atlet yang dipilih
                target_athletes = athletes if recipient_type == 'Semua Atlet' else selected_athletes
                
                for athlete in target_athletes:
                    if athlete not in assigned_programs:
                        assigned_programs[athlete] = {}
                    if date_str not in assigned_programs[athlete]:
                        assigned_programs[athlete][date_str] = []
                    assigned_programs[athlete][date_str].append(new_program)
                
                with open('assigned_programs.json', 'w') as f:
                    json.dump(assigned_programs, f)
                
                if recipient_type == 'Semua Atlet':
                    st.success('Program berhasil dibuat dan dikirim ke semua atlet!')
                else:
                    st.success(f'Program berhasil dibuat dan dikirim ke {len(selected_athletes)} atlet!')
                st.rerun()

    # Tampilkan program yang ditugaskan untuk atlet
    elif st.session_state.role == 'athlete':
        st.header('Kalender Program Latihan')
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox('Tahun', [2025], key='athlete_year')
        with col2:
            month = st.selectbox('Bulan', range(1, 13), format_func=lambda x: month_names[x], key='athlete_month')
        
        user_programs = assigned_programs.get(st.session_state.username, {})
        create_calendar(year, month, user_programs)

    # Tampilkan program yang perlu dievaluasi untuk pelatih
    if st.session_state.role == 'coach':
        # Load assigned programs
        with open('assigned_programs.json', 'r') as f:
            assigned_programs = json.load(f)
            
        st.header('Program Yang Perlu Dievaluasi')
        for athlete, programs in assigned_programs.items():
            for date_str, programs_list in programs.items():
                for program in programs_list:
                    if program.get('coach') == st.session_state.username and program.get('status') == 'Menunggu Evaluasi':
                        with st.expander(f"{program['name']} - {date_str} - Atlet: {athlete}"):
                            st.write(f"Deskripsi: {program['description']}")
                            st.write(f"Durasi: {program['duration']} jam")
                            st.write(f"Intensitas: {program['intensity']}")
                            
                            evaluation = st.text_area('Evaluasi', key=f"eval_{date_str}_{program['name']}_{athlete}")
                            if st.button('Kirim Evaluasi', key=f"send_eval_{date_str}_{program['name']}_{athlete}"):
                                program['evaluation'] = evaluation
                                program['status'] = 'Selesai'
                                with open('assigned_programs.json', 'w') as f:
                                    json.dump(assigned_programs, f)
                                st.success('Evaluasi berhasil dikirim!')
                                st.rerun()

        # Tampilkan daftar program yang ditugaskan
        st.header('Program Yang Ditugaskan')
        user_programs = assigned_programs.get(st.session_state.username, {})
        for date_str, programs_list in user_programs.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date.year == year and date.month == month:
                for program in programs_list:
                    with st.expander(f"{program['name']} - {date_str}"):
                        st.write(f"Deskripsi: {program['description']}")
                        st.write(f"Durasi: {program['duration']} jam")
                        st.write(f"Intensitas: {program['intensity']}")
                        st.write(f"Pelatih: {program['coach']}")
                        
                        # Tambahkan status program dan tombol selesai
                        program_status = program.get('status', 'Belum Selesai')
                        st.write(f"Status: {program_status}")
                        
                        if program_status == 'Belum Selesai':
                            if st.button('Tandai Selesai', key=f"complete_{date_str}_{program['name']}"):
                                program['status'] = 'Menunggu Evaluasi'
                                with open('assigned_programs.json', 'w') as f:
                                    json.dump(assigned_programs, f)
                                st.success('Program ditandai sebagai selesai!')
                                st.rerun()
                        
                        # Tampilkan evaluasi jika ada
                        if 'evaluation' in program:
                            st.write(f"Evaluasi Pelatih: {program['evaluation']}")
