const API_URL = '/api/v1';
let currentUser = null;

// Функции аутентификации
async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            alert('Регистрация успешна! Теперь вы можете войти.');
        } else {
            const error = await response.json();
            console.error(`Ошибка: ${error.detail}`);
        }
    } catch (error) {
        alert('Ошибка при регистрации');
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/conferences/`, {
            method: 'GET',
            headers: {
                'Authorization': `Basic ${btoa(`${username}:${password}`)}`,
            },
        });

        if (response.ok) {
            currentUser = { username, password };
            updateAuthUI();
            loadConferences();
        } else {
            console.error('Неверные учетные данные');
        }
    } catch (error) {
        alert('Ошибка при входе');
    }
}

function logout() {
    currentUser = null;
    updateAuthUI();
    document.getElementById('conferences').innerHTML = '';
}

function updateAuthUI() {
    const loginForm = document.getElementById('login-form');
    const userInfo = document.getElementById('user-info');
    const conferenceForm = document.getElementById('conference-form');

    if (currentUser) {
        loginForm.style.display = 'none';
        userInfo.style.display = 'block';
        conferenceForm.style.display = 'block';
        document.getElementById('current-user').textContent = currentUser.username;
    } else {
        loginForm.style.display = 'block';
        userInfo.style.display = 'none';
        conferenceForm.style.display = 'none';
    }
}

// Функции для работы с конференциями
async function loadConferences() {
    console.log('Начало загрузки конференций');
    try {
        const response = await fetch(`${API_URL}/conferences/`, {
            headers: {
                'Authorization': `Basic ${btoa(`${currentUser.username}:${currentUser.password}`)}`,
            },
        });

        if (response.ok) {
            const conferences = await response.json();
            console.log(`Получены конференции: ${conferences}`);
            displayConferences(conferences);
        } else {
            console.error('Ошибка при получении конференций:', response.status);
        }
    } catch (error) {
        console.error('Ошибка при загрузке конференций:', error);
    }
}

function displayConferences(conferences) {
    const container = document.getElementById('conferences');
    container.innerHTML = '';

    conferences.forEach(conference => {
        console.log(`Обработка конференции: ${JSON.stringify(conference, null, 2)}`);
        console.log(`ID конференции: ${conference.conference_id}`);
        
        const card = document.createElement('div');
        card.className = 'conference-card';
        
        // Создаем кнопки отдельно для лучшего контроля
        const editButton = document.createElement('button');
        editButton.className = 'edit-btn';
        editButton.textContent = 'Редактировать';
        editButton.onclick = () => editConference(conference.conference_id);
        
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-btn';
        deleteButton.textContent = 'Удалить';
        deleteButton.onclick = () => deleteConference(conference.conference_id);
        
        card.innerHTML = `
            <h3>${conference.title}</h3>
            <p>${conference.description}</p>
            <p>Начало: ${new Date(conference.start_time).toLocaleString()}</p>
            <p>Окончание: ${new Date(conference.end_time).toLocaleString()}</p>
            <p>Статус: ${conference.status}</p>
            <p>Макс. участников: ${conference.max_participants}</p>
            <div class="conference-actions"></div>
        `;
        
        // Добавляем кнопки в контейнер действий
        const actionsContainer = card.querySelector('.conference-actions');
        // actionsContainer.appendChild(editButton);
        actionsContainer.appendChild(deleteButton);
        
        container.appendChild(card);
    });
}

// Обработчик формы создания конференции
document.getElementById('new-conference-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const conference = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        start_time: document.getElementById('start-time').value,
        end_time: document.getElementById('end-time').value,
        meeting_link: document.getElementById('meeting-link').value,
        max_participants: parseInt(document.getElementById('max-participants').value),
        registration_deadline: document.getElementById('registration-deadline').value,
        timezone: document.getElementById('timezone').value,
        tags: document.getElementById('tags').value.split(',').map(tag => tag.trim()),
        status: 'scheduled'
    };

    try {
        const response = await fetch(`${API_URL}/conferences/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Basic ${btoa(`${currentUser.username}:${currentUser.password}`)}`,
            },
            body: JSON.stringify(conference),
        });

        if (response.ok) {
            e.target.reset();
            loadConferences();
        } else {
            const error = await response.json();
            console.error(`Ошибка: ${error.detail}`);
        }
    } catch (error) {
        alert('Ошибка при создании конференции');
    }
});

async function deleteConference(conferenceId) {
    console.log(`Попытка удаления конференции с ID: ${conferenceId}`);
    if (!conferenceId) {
        console.error('ID конференции не определен');
        return;
    }
    
    if (!confirm('Вы уверены, что хотите удалить эту конференцию?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/conferences/${conferenceId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Basic ${btoa(`${currentUser.username}:${currentUser.password}`)}`,
            },
        });

        if (response.ok) {
            loadConferences();
        } else {
            alert('Ошибка при удалении конференции');
        }
    } catch (error) {
        console.error('Ошибка при удалении конференции:', error);
    }
}

async function editConference(conferenceId) {
    try {
        const response = await fetch(`${API_URL}/conferences/${conferenceId}`, {
            headers: {
                'Authorization': `Basic ${btoa(`${currentUser.username}:${currentUser.password}`)}`,
            },
        });

        if (response.ok) {
            const conference = await response.json();
            console.log(`Получены данные конференции: ${JSON.stringify(conference, null, 2)}`);
            // Заполняем форму данными конференции
            document.getElementById('title').value = conference.title;
            document.getElementById('description').value = conference.description;
            document.getElementById('start-time').value = conference.start_time.slice(0, 16);
            document.getElementById('end-time').value = conference.end_time.slice(0, 16);
            document.getElementById('meeting-link').value = conference.meeting_link || '';
            document.getElementById('max-participants').value = conference.max_participants;
            document.getElementById('registration-deadline').value = conference.registration_deadline.slice(0, 16);
            document.getElementById('timezone').value = conference.timezone;
            document.getElementById('tags').value = conference.tags.join(', ');

            // Прокручиваем к форме
            document.getElementById('conference-form').scrollIntoView({ behavior: 'smooth' });
        }
    } catch (error) {
        alert('Ошибка при загрузке данных конференции');
    }
} 