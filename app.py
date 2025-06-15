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
    .program-completed {
        background-color: #e6ffe6 !important;
        border: 1px solid #4CAF50 !important;
    }
    .program-completed .calendar-day-program {
        background-color: #b3ffb3 !important;
        color: #1a661a !important;
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

# Fungsi untuk menghapus pengguna
def delete_user(username):
    users = load_users()
    if username in users:
        del users[username]
        with open('users.json', 'w') as f:
            json.dump(users, f)
        return True
    return False

# Fungsi untuk mengupdate pengguna
def update_user(username, new_data):
    users = load_users()
    if username in users:
        if 'password' in new_data and new_data['password']:
            new_data['password'] = hash_password(new_data['password'])
        users[username].update(new_data)
        with open('users.json', 'w') as f:
            json.dump(users, f)
        return True
    return False

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
                        # Cek apakah program sudah selesai dan dievaluasi
                        has_completed_program = any('evaluation' in p for p in progs)
                        program_class = 'has-program program-completed' if has_completed_program else 'has-program'
                        
                        st.markdown(f"""
                        <style>
                        [data-testid="column"]:has(div.{program_class}) {{
                            background-color: {"#4CAF50" if has_completed_program else "#0066cc"};
                            border-radius: 5px;
                            padding: 5px;
                            margin: 2px;
                        }}
                        </style>
                        """, unsafe_allow_html=True)
                        st.markdown(f"<div class='{program_class}'>", unsafe_allow_html=True)
                        calendar_color = "#4CAF50" if has_completed_program else "#0066cc"
                        st.markdown(f"<div class='calendar-day' style='text-align: center; color: {calendar_color}; font-size: 1.1em; font-weight: bold;'>{day_names[i]} {day}</div>", unsafe_allow_html=True)
                        if has_completed_program:
                            st.markdown(f"<div style='text-align: center; color: #4CAF50; font-weight: bold;'>✓ Selesai</div>", unsafe_allow_html=True)
                        for idx, prog in enumerate(progs):
                            with st.expander(prog['name']):
                                users = load_users()
                                # Tampilkan nama pelatih
                                coach_name = users[prog['coach']]['name'] if prog['coach'] in users else 'Tidak diketahui'
                                st.write(f"Pelatih: {coach_name}")
                                
                                # Tampilkan nama atlet
                                athlete_name = ''
                                for username, data in users.items():
                                    if data['role'] == 'athlete' and username in assigned_programs and date_str in assigned_programs[username]:
                                        for p in assigned_programs[username][date_str]:
                                            if p['name'] == prog['name'] and p['coach'] == prog['coach']:
                                                athlete_name = data['name']
                                                break
                                st.write(f"Atlet: {athlete_name if athlete_name else 'Belum ditugaskan'}")
                                
                                st.write(f"Deskripsi: {prog['description']}")
                                st.write(f"Durasi: {prog['duration']} jam")
                                st.write(f"Intensitas: {prog['intensity']}")
                                
                                # Tambahkan status program dan tombol selesai
                                program_status = prog.get('status', 'Belum Selesai')
                                st.write(f"Status: {program_status}")
                                
                                if program_status == 'Belum Selesai':
                                    # Tambahkan username dan indeks ke key untuk membuatnya unik
                                    button_key = f"complete_{date_str}_{prog['name']}_{st.session_state.username}_{idx}_calendar"
                                    if st.button('Tandai Selesai', key=button_key):
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
        role = 'athlete' # Registrasi hanya untuk atlet
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
    elif st.session_state.role == 'admin':
        st.title('Dashboard Admin')
        st.write(f'Selamat datang, {st.session_state.username}!')
        
        # Tampilkan dan edit profil admin
        st.header('Profil Admin')
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
        
        st.header('Manajemen Pengguna')
        users = load_users()
        
        # Tab untuk menampilkan daftar pelatih dan atlet
        user_tab1, user_tab2 = st.tabs(['Daftar Pelatih', 'Daftar Atlet'])
        
        with user_tab1:
            coaches = {username: data for username, data in users.items() if data['role'] == 'coach'}
            st.subheader('Daftar Pelatih')
            
            # Tombol untuk menambah pelatih baru
            if st.button('Tambah Pelatih Baru'):
                st.session_state.add_coach = True
                st.rerun()
            
            # Form untuk menambah pelatih baru
            if 'add_coach' in st.session_state and st.session_state.add_coach:
                with st.form('add_coach_form'):
                    new_username = st.text_input('Username')
                    new_password = st.text_input('Password', type='password')
                    new_name = st.text_input('Nama Lengkap')
                    new_phone = st.text_input('Nomor Telepon')
                    
                    if st.form_submit_button('Simpan'):
                        if save_user(new_username, new_password, 'coach', new_name, new_phone):
                            st.success('Pelatih berhasil ditambahkan!')
                            st.session_state.add_coach = False
                            st.rerun()
                        else:
                            st.error('Username sudah digunakan')
            
            # Tampilkan daftar pelatih
            for username, data in coaches.items():
                with st.expander(f"Pelatih: {data['name']} ({username})"):
                    with st.form(f'edit_coach_{username}'):
                        edit_name = st.text_input('Nama Lengkap', value=data['name'])
                        edit_phone = st.text_input('Nomor Telepon', value=data['phone'])
                        edit_password = st.text_input('Password Baru (kosongkan jika tidak ingin mengubah)', type='password')
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button('Simpan Perubahan'):
                                update_data = {
                                    'name': edit_name,
                                    'phone': edit_phone
                                }
                                if edit_password:
                                    update_data['password'] = edit_password
                                if update_user(username, update_data):
                                    st.success('Data pelatih berhasil diperbarui!')
                                    st.rerun()
                        
                        with col2:
                            if st.form_submit_button('Hapus Pelatih'):
                                if delete_user(username):
                                    st.success('Pelatih berhasil dihapus!')
                                    st.rerun()
        
        with user_tab2:
            athletes = {username: data for username, data in users.items() if data['role'] == 'athlete'}
            st.subheader('Daftar Atlet')
            
            # Tombol untuk menambah atlet baru
            if st.button('Tambah Atlet Baru'):
                st.session_state.add_athlete = True
                st.rerun()
            
            # Form untuk menambah atlet baru
            if 'add_athlete' in st.session_state and st.session_state.add_athlete:
                with st.form('add_athlete_form'):
                    new_username = st.text_input('Username')
                    new_password = st.text_input('Password', type='password')
                    new_name = st.text_input('Nama Lengkap')
                    new_phone = st.text_input('Nomor Telepon')
                    
                    if st.form_submit_button('Simpan'):
                        if save_user(new_username, new_password, 'athlete', new_name, new_phone):
                            st.success('Atlet berhasil ditambahkan!')
                            st.session_state.add_athlete = False
                            st.rerun()
                        else:
                            st.error('Username sudah digunakan')
            
            # Tampilkan daftar atlet
            for username, data in athletes.items():
                with st.expander(f"Atlet: {data['name']} ({username})"):
                    with st.form(f'edit_athlete_{username}'):
                        edit_name = st.text_input('Nama Lengkap', value=data['name'])
                        edit_phone = st.text_input('Nomor Telepon', value=data['phone'])
                        edit_password = st.text_input('Password Baru (kosongkan jika tidak ingin mengubah)', type='password')
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button('Simpan Perubahan'):
                                update_data = {
                                    'name': edit_name,
                                    'phone': edit_phone
                                }
                                if edit_password:
                                    update_data['password'] = edit_password
                                if update_user(username, update_data):
                                    st.success('Data atlet berhasil diperbarui!')
                                    st.rerun()
                        
                        with col2:
                            if st.form_submit_button('Hapus Atlet'):
                                if delete_user(username):
                                    st.success('Atlet berhasil dihapus!')
                                    st.rerun()
    
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
                        # Cari nama atlet dari assigned_programs
                        athlete_name = ''
                        for athlete, programs in assigned_programs.items():
                            if date in programs and any(p['name'] == prog['name'] and p['coach'] == prog['coach'] for p in programs[date]):
                                athlete_name = load_users()[athlete]['name']
                                break
                        
                        st.write(f"Atlet: {athlete_name if athlete_name else 'Belum ditugaskan'}")
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
                            # Cek apakah program memiliki atlet
                            has_athlete = False
                            for athlete, athlete_programs in assigned_programs.items():
                                if date in athlete_programs and any(p['name'] == prog['name'] and p['coach'] == prog['coach'] for p in athlete_programs[date]):
                                    has_athlete = True
                                    break

                            if st.button('Hapus Program', key=f'delete_{edit_key}'):
                                # Hapus program dari programs.json jika tanggal ada
                                if date in programs:
                                    programs[date].pop(i)
                                    if not programs[date]:
                                        del programs[date]
                                    with open('programs.json', 'w') as f:
                                        json.dump(programs, f)
                                    
                                    # Hapus program dari assigned_programs.json jika ada
                                    for athlete, athlete_programs in assigned_programs.items():
                                        if date in athlete_programs:
                                            athlete_programs[date] = [p for p in athlete_programs[date] if not (p['name'] == prog['name'] and p['coach'] == prog['coach'])]
                                            if not athlete_programs[date]:
                                                del athlete_programs[date]
                                    
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
            intensity = st.selectbox('Intensitas', ['Rendah', 'Sedang', 'Tinggi'], key='intensity_select')
            
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
                target_athletes = athletes if st.session_state.recipient_type == 'Semua Atlet' else selected_athletes
                
                for athlete in target_athletes:
                    if athlete not in assigned_programs:
                        assigned_programs[athlete] = {}
                    if date_str not in assigned_programs[athlete]:
                        assigned_programs[athlete][date_str] = []
                    assigned_programs[athlete][date_str].append(new_program)
                
                with open('assigned_programs.json', 'w') as f:
                    json.dump(assigned_programs, f)
                
                if st.session_state.recipient_type == 'Semua Atlet':
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
        has_programs_to_evaluate = False
        for athlete, programs in assigned_programs.items():
            for date_str, programs_list in programs.items():
                for idx, program in enumerate(programs_list):
                    if program.get('coach') == st.session_state.username and program.get('status') == 'Menunggu Evaluasi':
                        has_programs_to_evaluate = True
                        with st.expander(f"{program['name']} - {date_str} - Atlet: {athlete}"):
                            st.write(f"Deskripsi: {program['description']}")
                            st.write(f"Durasi: {program['duration']} jam")
                            st.write(f"Intensitas: {program['intensity']}")
                            
                            evaluation = st.text_area('Evaluasi', key=f"eval_{date_str}_{program['name']}_{athlete}_{idx}")
                            if st.button('Kirim Evaluasi', key=f"send_eval_{date_str}_{program['name']}_{athlete}_{idx}"):
                                program['evaluation'] = evaluation
                                program['status'] = 'Selesai'
                                with open('assigned_programs.json', 'w') as f:
                                    json.dump(assigned_programs, f)
                                st.success('Evaluasi berhasil dikirim!')
                                st.rerun()
        
        if not has_programs_to_evaluate:
            st.info('Tidak ada program yang perlu dievaluasi saat ini.')

        # Tampilkan daftar program yang ditugaskan
        st.header('Program Yang Ditugaskan')
        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox('Tahun', [2025], key='coach_year')
        with col2:
            selected_month = st.selectbox('Bulan', range(1, 13), format_func=lambda x: month_names[x], key='coach_month')
            
        user_programs = assigned_programs.get(st.session_state.username, {})
        for date_str, programs_list in user_programs.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date.year == selected_year and date.month == selected_month:
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