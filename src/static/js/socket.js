var room_id = document.querySelector('#room-id').value;
var user_name = document.querySelector('#user-name').value;
var chat_box = document.querySelector('#chat-box');
var online_list = document.querySelector('#online-list');
chat_box.scrollTop = chat_box.scrollHeight;

var ws_protocol = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_protocol + '://' + window.location.host + "/room/" + room_id + "/";
var socket = new ReconnectingWebSocket(ws_path);

socket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    if (data['type'] == 'message') {
        createMessageDOM(data['sender'], data['message']);
    } else if (data['type'] == 'user_joined') {
        userJoinedOrLeftDOM(data['user'] + " joined the room.")
        if (user_name != data['user']) {
            addList(data['user'])
        }
    } else {
        userJoinedOrLeftDOM(data['user'] + " left the room.")
        deleteList(data['user'])
    }
};

function addList(user) {
    var list = document.createElement('li');
    list.className = 'list-group-item list-group-item-action'
    list.appendChild(document.createTextNode(user))
    online_list.appendChild(list)
}

function deleteList(user) {
    lists = online_list.childNodes;
    for (var i = 0; i < lists.length; i++) {
        if (lists[i].innerHTML == user) {
            online_list.removeChild(lists[i]);
        }
    }
}

function userJoinedOrLeftDOM(msg) {
    var paragraph = document.createElement('p');
    paragraph.className = "text-center font-weight-light font-italic";
    paragraph.appendChild(document.createTextNode(msg));
    chat_box.appendChild(paragraph);

    chat_box.scrollTop = chat_box.scrollHeight;
}

function createMessageDOM(sender, message) {
    var paragraph = document.createElement('p');
    paragraph.className = 'font-weight-bold m-0';
    paragraph.appendChild(document.createTextNode(sender));
    chat_box.appendChild(paragraph);

    var message_paragraph = document.createElement('p');
    message_paragraph.className = 'text-secondary m-0';
    message_paragraph.appendChild(document.createTextNode(message));
    chat_box.appendChild(message_paragraph);

    var horizontal_bar = document.createElement('hr');
    horizontal_bar.className = 'my-1';
    chat_box.appendChild(horizontal_bar);

    chat_box.scrollTop = chat_box.scrollHeight;
}


socket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#message-input').focus();
document.querySelector('#message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {
        document.querySelector('#message-send-input').click();
    }
};

document.querySelector('#message-send-input').onclick = function (e) {
    var messageInputDom = document.querySelector('#message-input');
    var message = messageInputDom.value;
    socket.send(JSON.stringify({
        'type': 'message',
        'message': message
    }));

    messageInputDom.value = '';
};