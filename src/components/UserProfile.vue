<template>
  <div class="profile-page" :class="{ 'dark-mode': isDarkMode }">
    <div class="profile-header-row">
      <button class="back-btn" @click="$emit('back')">
        <span class="arrow">←</span> Back
      </button>
    </div>
    <div class="profile-row">
      <div class="profile-card">
        <button class="edit-profile-btn" @click="openEditModal">Edit</button>
        <h2>Profile</h2>
        <hr />
        <div class="profile-main-row">
          <div class="avatar-block">
            <div class="avatar-wrapper">
              <img v-if="userAvatar" :src="userAvatar" alt="User Avatar" class="current-avatar" />
              <div v-else class="avatar-placeholder">No Avatar</div>
            </div>
          </div>
          <div class="profile-info-view">
            <div class="info-row">
              <span class="info-label">Username</span>
              <span class="info-value">{{ username }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Email</span>
              <span class="info-value">{{ email }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="stats-card">
        <h2>Task Statistics</h2>
        <hr />
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon stat-bar">
              <svg width="32" height="32" viewBox="0 0 24 24"><rect x="3" y="13" width="4" height="8" fill="#e0f2f1"/><rect x="10" y="9" width="4" height="12" fill="#009688"/><rect x="17" y="5" width="4" height="16" fill="#43a047"/></svg>
            </div>
            <div class="stat-value">{{ totalTasks }}</div>
            <div class="stat-label">Total Tasks</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon stat-check">
              <svg width="32" height="32" viewBox="0 0 24 24"><rect width="24" height="24" fill="none"/><path d="M9 16.2l-3.5-3.5 1.4-1.4L9 13.4l7.1-7.1 1.4 1.4z" fill="#00e676"/></svg>
            </div>
            <div class="stat-value">{{ completedTasks }}</div>
            <div class="stat-label">Completed</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon stat-star">
              <svg width="32" height="32" viewBox="0 0 24 24"><polygon points="12,17.27 18.18,21 16.54,13.97 22,9.24 14.81,8.63 12,2 9.19,8.63 2,9.24 7.46,13.97 5.82,21" fill="#ffd600"/></svg>
            </div>
            <div class="stat-value">{{ importantTasks }}</div>
            <div class="stat-label">Important</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon stat-rate">
              <svg width="32" height="32" viewBox="0 0 24 24"><rect width="24" height="24" fill="none"/><path d="M4 17l6-6 4 4 6-6" stroke="#42a5f5" stroke-width="2" fill="none"/><circle cx="12" cy="12" r="10" stroke="#42a5f5" stroke-width="2" fill="none"/></svg>
            </div>
            <div class="stat-value stat-blue">{{ completionRate }}%</div>
            <div class="stat-label">Completion Rate</div>
          </div>
        </div>
      </div>
    </div>
    <div class="settings-menu-below">
      <button class="settings-btn" @click="toggleTheme">
        <span class="icon">{{ isDarkMode ? '' : '' }}</span>
        {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
      </button>
      <button class="settings-btn logout-btn" @click="$emit('logout')">
        <span class="icon"></span> Logout
      </button>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content profile-edit-modal">
        <h2>Edit Profile</h2>
        <form @submit.prevent="saveProfileEdit">
          <div class="edit-avatar-block">
            <img v-if="editAvatar" :src="editAvatar" alt="Avatar" class="current-avatar" />
            <div v-else class="avatar-placeholder">No Avatar</div>
            <input type="file" ref="editFileInput" accept="image/*" style="display:none" @change="handleEditAvatarChange" />
            <button type="button" class="change-avatar-btn" @click="$refs.editFileInput.click()">Change Avatar</button>
          </div>
          <div class="form-group">
            <label for="edit-username">Username</label>
            <input id="edit-username" v-model="editUsername" type="text" required />
          </div>
          <div class="form-group">
            <label for="edit-email">Email</label>
            <input id="edit-email" v-model="editEmail" type="email" required />
          </div>
          <div class="modal-actions">
            <button type="button" class="modal-cancel" @click="showEditModal = false">Cancel</button>
            <button type="submit" class="modal-save">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfile',
  props: {
    tasks: {
      type: Array,
      required: true
    },
    isDarkMode: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      username: localStorage.getItem('username') || '',
      email: localStorage.getItem('email') || '',
      userAvatar: localStorage.getItem('userAvatar') || '',
      showEditModal: false,
      editUsername: localStorage.getItem('username') || '',
      editEmail: localStorage.getItem('email') || '',
      editAvatar: localStorage.getItem('userAvatar') || ''
    }
  },
  computed: {
    totalTasks() {
      return this.tasks.length
    },
    completedTasks() {
      return this.tasks.filter(task => task.completed).length
    },
    importantTasks() {
      return this.tasks.filter(task => task.priority === 'High').length
    },
    completionRate() {
      if (this.totalTasks === 0) return 0
      return Math.round((this.completedTasks / this.totalTasks) * 100)
    }
  },
  methods: {
    handleAvatarChange(event) {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.userAvatar = e.target.result
        }
        reader.readAsDataURL(file)
      }
    },
    saveProfile() {
      localStorage.setItem('username', this.username)
      localStorage.setItem('email', this.email)
      localStorage.setItem('userAvatar', this.userAvatar)
      this.$emit('profile-updated', {
        username: this.username,
        email: this.email,
        avatar: this.userAvatar
      })
    },
    toggleTheme() {
      this.$emit('theme-changed')
    },
    handleEditAvatarChange(event) {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.editAvatar = e.target.result
        }
        reader.readAsDataURL(file)
      }
    },
    saveProfileEdit() {
      this.username = this.editUsername
      this.email = this.editEmail
      this.userAvatar = this.editAvatar
      localStorage.setItem('username', this.username)
      localStorage.setItem('email', this.email)
      localStorage.setItem('userAvatar', this.userAvatar)
      this.$emit('profile-updated', {
        username: this.username,
        email: this.email,
        avatar: this.userAvatar
      })
      this.showEditModal = false
    },
    openEditModal() {
      this.editUsername = this.username;
      this.editEmail = this.email;
      this.editAvatar = this.userAvatar;
      this.showEditModal = true;
    }
  }
}
</script>

<style>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
  padding: 32px 0 0 0;
  background: transparent;
}

.profile-row {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: stretch;
  gap: 24px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-card, .stats-card {
  background: linear-gradient(135deg, #f8fafc 0%, #e3e8ef 100%);
  border-radius: 24px;
  box-shadow: 0 6px 32px rgba(30,40,90,0.13), 0 1.5px 8px rgba(30,40,90,0.08);
  border: 1.5px solid #e3e8ef;
  padding: 48px 44px 36px 44px;
  min-width: 400px;
  max-width: 700px;
  width: 100%;
  color: #222;
  position: relative;
  flex: 1 1 0;
  box-sizing: border-box;
  margin: 0;
  transition: box-shadow 0.22s, transform 0.22s;
}
.profile-card:hover, .stats-card:hover {
  box-shadow: 0 12px 40px rgba(30,40,90,0.18), 0 2px 12px rgba(30,40,90,0.10);
  transform: translateY(-2px) scale(1.012);
}
.dark-mode .profile-card, .dark-mode .stats-card {
  background: linear-gradient(135deg, #23272f 0%, #181a20 100%);
  color: #fff;
  border: 1.5px solid #23272f;
  box-shadow: 0 6px 32px rgba(0,0,0,0.22), 0 1.5px 8px rgba(0,0,0,0.13);
}
.dark-mode .profile-card:hover, .dark-mode .stats-card:hover {
  box-shadow: 0 12px 40px rgba(0,0,0,0.28), 0 2px 12px rgba(0,0,0,0.16);
  transform: translateY(-2px) scale(1.012);
}

h2 {
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 12px;
  color: #222;
}

.dark-mode h2 {
  color: #fff;
}

hr {
  border: none;
  border-top: 1px solid #000000;
  margin-bottom: 24px;
}

.dark-mode hr {
  border-top: 1px solid #444;
}

.profile-main-row {
  display: flex;
  align-items: flex-start;
  gap: 32px;
  flex-wrap: wrap;
}

.avatar-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
  flex: 0 0 120px;
}

.avatar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.current-avatar, .avatar-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 4px;
  background: #f5f5f5;
}
.current-avatar {
  border: 2px solid #e0f2f1;
}
.avatar-placeholder {
  border: 2px dashed #e0f2f1;
  color: #e0f2f1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1em;
}
.dark-mode .current-avatar, .dark-mode .avatar-placeholder {
  background: #181818;
}

.change-avatar-btn {
  background: none;
  border: 1.5px solid #e0f2f1;
  color: #009688;
  border-radius: 24px;
  padding: 6px 18px;
  font-size: 1em;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.dark-mode .change-avatar-btn {
  color: #e0f2f1;
}
.change-avatar-btn:hover {
  background: #e0f2f1;
  color: #009688;
}
.dark-mode .change-avatar-btn:hover {
  background: #e0f2f1;
  color: #181818;
}

.profile-info-view {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-top: 12px;
  min-width: 180px;
  width: 100%;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.info-label {
  font-weight: 600;
  color: #706c6c;
  font-size: 1em;
  margin-bottom: 0;
}
.dark-mode .info-label {
  color: #bdbdbd;
}
.info-value {
  font-size: 1.22em;
  color: #000000;
  font-weight: 600;
  margin-top: 0;
  background: none;
  border: none;
  border-radius: 0;
  padding: 0;
  text-align: left;
  box-shadow: none;
}
.dark-mode .info-value {
  color: #fff;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-top: 18px;
}

.stat-card {
  background: #f5f5f5;
  border-radius: 12px;
  padding: 18px 10px 14px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  min-width: 0;
  min-height: 100px;
  width: 100%;
  box-sizing: border-box;
}
.dark-mode .stat-card {
  background: #181818;
  box-shadow: 0 1px 4px rgba(0,0,0,0.10);
}

.stat-icon {
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 1.5em;
  font-weight: bold;
  color: #009688;
  margin-bottom: 2px;
}
.dark-mode .stat-value {
  color: #43a047;
}

.stat-blue {
  color: #42a5f5;
}

.stat-label {
  font-size: 1em;
  color: #888;
  font-weight: 500;
  text-align: center;
}
.dark-mode .stat-label {
  color: #bdbdbd;
}

@media (max-width: 1100px) {
  .profile-row {
    flex-direction: column;
    align-items: center;
    gap: 18px;
    width: 100%;
    max-width: 100vw;
  }
  .profile-card, .stats-card {
    min-width: 0;
    max-width: 100%;
    width: 98vw;
    padding: 24px 8px 18px 8px;
  }
  .settings-menu-below {
    max-width: 100vw;
  }
}

@media (max-width: 600px) {
  .profile-page {
    padding: 8px 0;
    gap: 12px;
  }
  .profile-card, .stats-card {
    padding: 12px 2vw 10px 2vw;
    border-radius: 8px;
  }
  h2 {
    font-size: 1.2em;
  }
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  .stat-card {
    padding: 10px 4px 8px 4px;
    border-radius: 6px;
    min-height: 70px;
  }
  .current-avatar, .avatar-placeholder {
    width: 80px;
    height: 80px;
    font-size: 0.9em;
  }
  .avatar-block {
    min-width: 80px;
    flex: 0 0 80px;
  }
  .change-avatar-btn {
    font-size: 0.9em;
    padding: 4px 10px;
    border-radius: 14px;
  }
  .save-btn {
    font-size: 1em;
    padding: 10px 0;
    border-radius: 6px;
  }
}

.settings-menu,
.settings-section {
  display: none;
}
.settings-menu-below {
  display: flex;
  flex-direction: row;
  gap: 18px;
  justify-content: center;
  margin: 24px 0 0 0;
  width: 100%;
  background: #f8fafd;
  border-radius: 16px;
  box-shadow: 0 1px 8px rgba(0,0,0,0.08);
  padding: 12px 0;
  max-width: 900px;
}
.dark-mode .settings-menu-below {
  background: #23272f;
  box-shadow: 0 1px 8px rgba(0,0,0,0.18);
}
.settings-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f5f5f5;
  color: #222;
  border: none;
  border-radius: 10px;
  padding: 10px 20px 10px 10px;
  font-size: 1.08em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(30,40,90,0.06);
  outline: none;
}
.settings-btn:hover {
  background: #e3f2fd;
  color: #1976d2;
  box-shadow: 0 4px 16px rgba(30,40,90,0.13);
}
.dark-mode .settings-btn {
  background: #23272f;
  color: #f5f5f5;
  box-shadow: 0 2px 8px rgba(0,0,0,0.13);
}
.dark-mode .settings-btn:hover {
  background: #333b4a;
  color: #90caf9;
}
.logout-btn {
  color: #fff;
  background: #e53935;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(229,57,53,0.13);
}
.logout-btn:hover {
  background: #b71c1c;
  color: #fff;
}
.dark-mode .logout-btn {
  color: #fff;
  background: #c62828;
  box-shadow: 0 2px 8px rgba(198,40,40,0.18);
}
.dark-mode .logout-btn:hover {
  background: #b71c1c;
  color: #fff;
}
@media (max-width: 800px) {
  .settings-menu-below {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
    margin: 10px 0 0 0;
    padding: 6px 0;
  }
  .profile-card, .stats-card {
    min-width: 0;
    max-width: 98vw;
    padding: 18px 4vw 12px 4vw;
  }
}

.profile-header-row {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 17px;
}
.back-btn {
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 7px 20px 7px 14px;
  font-size: 0.95em;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(30,40,90,0.08);
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-left: 23px;
}
.back-btn .arrow {
  font-size: 1em;
  font-weight: bold;
  margin-right: 3px;
  display: flex;
  align-items: center;
}
.back-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
  color: #fff;
  box-shadow: 0 4px 16px rgba(30,40,90,0.16);
}
.dark-mode .back-btn {
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: #fff;
}
.dark-mode .back-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
}
.edit-profile-btn {
  position: absolute;
  top: 32px;
  right: 32px;
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 10px 22px 10px 22px;
  font-size: 1.08em;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(30,40,90,0.08);
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 8px;
}
.edit-profile-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
  color: #fff;
  box-shadow: 0 4px 16px rgba(30,40,90,0.12);
}
.dark-mode .edit-profile-btn {
  background: linear-gradient(135deg, #009688,rgb(56, 112, 59));
  color: #fff;
}
.dark-mode .edit-profile-btn:hover {
  background: linear-gradient(135deg, #43a047, #009688);
  color: #fff;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(30,40,90,0.32);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content.profile-edit-modal {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(30,40,90,0.18);
  padding: 48px 36px 36px 36px;
  min-width: 320px;
  max-width: 98vw;
  width: 400px;
  color: #222;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.dark-mode .modal-content.profile-edit-modal {
  background: #23272f;
  color: #fff;
  box-shadow: 0 8px 32px rgba(0,0,0,0.22);
}
.edit-avatar-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 28px;
}
.edit-avatar-block .current-avatar {
  border: 3px solidrgba(56, 250, 137, 0.28);
  box-shadow: 0 2px 12px rgba(30,40,90,0.13);
  width: 120px;
  height: 120px;
  margin-bottom: 10px;
}
.edit-avatar-block .avatar-placeholder {
  border: 3px dashedrgb(56, 250, 117);
  color: #3887fa;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1em;
  margin-bottom: 10px;
}
.change-avatar-btn {
  background: #3887fa;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 10px 28px;
  font-size: 1.1em;
  font-weight: 500;
  cursor: pointer;
  margin-top: 0;
  margin-bottom: 0;
  transition: background 0.2s, color 0.2s;
}
.change-avatar-btn:hover {
  background: #1976d2;
  color: #fff;
}
.dark-mode .change-avatar-btn {
  background: #1976d2;
  color: #fff;
}
.dark-mode .change-avatar-btn:hover {
  background: #3887fa;
  color: #fff;
}
.profile-edit-modal form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.profile-edit-modal .form-group {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 22px;
}
.profile-edit-modal label {
  min-width: 110px;
  font-weight: 700;
  color: #222;
  font-size: 1.18em;
  letter-spacing: 0.01em;
  margin-bottom: 0;
}
.dark-mode .profile-edit-modal label {
  color: #fff;
}
.profile-edit-modal input[type="text"],
.profile-edit-modal input[type="email"] {
  flex: 1;
  padding: 14px 18px;
  border-radius: 10px;
  border: 1.5px solid #eee;
  background: #f8fafc;
  color: #222;
  font-size: 1.13em;
  outline: none;
  box-sizing: border-box;
  box-shadow: 0 1.5px 8px rgba(30,40,90,0.06);
  transition: border 0.2s, box-shadow 0.2s, background 0.2s;
  vertical-align: middle;
  margin-bottom: 0;
}
.dark-mode .profile-edit-modal input[type="text"],
.dark-mode .profile-edit-modal input[type="email"] {
  background: #23242a;
  color: #fff;
  border: 1.5px solid #333;
}
.profile-edit-modal input:focus {
  border: 2px solid #3887fa;
  box-shadow: 0 2px 12px rgba(56,135,250,0.13);
  background: #fff;
}
.dark-mode .profile-edit-modal input:focus {
  background: #23272f;
  border: 2px solid #6ec6ff;
  box-shadow: 0 2px 12px rgba(110,198,255,0.13);
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 24px;
}
.modal-cancel {
  background: #eee;
  color: #333;
  border: none;
  border-radius: 8px;
  padding: 10px 28px;
  font-size: 1.08em;
  cursor: pointer;
  transition: background 0.2s;
}
.modal-cancel:hover {
  background: #e3e8ef;
}
.modal-save {
  background: #3887fa;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 32px;
  font-size: 1.08em;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.modal-save:hover {
  background: #1976d2;
}
.dark-mode .modal-cancel {
  background: #23272f;
  color: #bdbdbd;
}
.dark-mode .modal-cancel:hover {
  background: #333;
}
.dark-mode .modal-save {
  background: #1976d2;
  color: #fff;
}
.dark-mode .modal-save:hover {
  background: #3887fa;
}
</style> 