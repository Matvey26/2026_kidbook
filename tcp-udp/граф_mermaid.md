graph TD
    %% Центральные понятия
    TCP["TCP\nTransmission Control Protocol\nQ8803"]
    UDP["UDP\nUser Datagram Protocol\nQ11163"]

    %% Уровни модели
    OSI["Модель OSI"]
    TRANSPORT["Транспортный уровень\nQ209372"]
    TCPIP["Стек TCP/IP\nQ81414"]

    %% Механизмы TCP
    HANDSHAKE["3-way handshake\nQ548838"]
    SYN["SYN-пакет"]
    ACK["ACK-пакет"]
    SYNACK["SYN-ACK пакет"]
    CONN["Connection-oriented\nQ1771161"]

    %% Механизмы UDP
    CONNLESS["Connectionless\nQ727896"]
    DATAGRAM["Датаграмма"]

    %% Общие понятия
    PACKET["Пакет данных"]
    PORT["Порт"]
    SOCKET["Сокет"]
    IP["IP-адрес\nQ11135"]

    %% Протоколы поверх TCP
    HTTP["HTTP/HTTPS\nQ8777"]
    WEBSOCKET["WebSocket\nQ859938"]
    DNSTCP["DNS over TCP\nQ112255512"]

    %% Протоколы поверх UDP
    DNS["DNS\nQ10261"]
    DHCP["DHCP\nQ11166"]
    RTP["RTP — видео/аудио\nQ321213"]

    %% Соседи по уровню
    QUIC["QUIC\nQ7265601"]
    SCTP["SCTP\nQ576997"]

    %% Иерархические связи (сверху вниз)
    OSI -->|"содержит"| TRANSPORT
    TRANSPORT -->|"включает"| TCP
    TRANSPORT -->|"включает"| UDP
    TRANSPORT -->|"включает"| QUIC
    TRANSPORT -->|"включает"| SCTP
    TCPIP -->|"содержит"| TCP
    TCPIP -->|"содержит"| UDP

    %% Свойства TCP
    TCP -->|"обладает свойством"| CONN
    TCP -->|"использует"| HANDSHAKE
    HANDSHAKE -->|"состоит из"| SYN
    HANDSHAKE -->|"состоит из"| SYNACK
    HANDSHAKE -->|"состоит из"| ACK

    %% Свойства UDP
    UDP -->|"обладает свойством"| CONNLESS
    UDP -->|"передаёт"| DATAGRAM

    %% Общие механизмы
    TCP -->|"адресуется через"| PORT
    UDP -->|"адресуется через"| PORT
    TCP -->|"адресуется через"| IP
    UDP -->|"адресуется через"| IP
    PORT -->|"вместе с IP образует"| SOCKET
    TCP -->|"передаёт"| PACKET
    UDP -->|"передаёт"| PACKET

    %% Горизонтальные связи — что работает поверх
    HTTP -->|"работает поверх"| TCP
    WEBSOCKET -->|"работает поверх"| TCP
    DNSTCP -->|"работает поверх"| TCP
    DNS -->|"работает поверх"| UDP
    DHCP -->|"работает поверх"| UDP
    RTP -->|"работает поверх"| UDP

    %% Горизонтальные связи — сравнение
    TCP <-->|"надёжнее, но медленнее"| UDP
    QUIC -->|"объединяет скорость UDP\nи надёжность TCP"| TCP
    QUIC -->|"объединяет скорость UDP\nи надёжность TCP"| UDP

    %% Стили
    style TCP fill:#4a90d9,color:#fff
    style UDP fill:#e67e22,color:#fff
    style TRANSPORT fill:#27ae60,color:#fff
    style HANDSHAKE fill:#8e44ad,color:#fff
    style QUIC fill:#c0392b,color:#fff
