import { useState, useEffect } from 'react'
import './UserSession.css'

export function ChatBotEmoji() {
    const [emotion, setEmotion] = useState("normal");
    const [hovered, setHovered] = useState(false);

  useEffect(() => {
    const emotions = ["normal", "wink", "surprised"];

    const interval = setInterval(() => {
      if (!hovered) {
        const randomEmotion =
          emotions[Math.floor(Math.random() * emotions.length)];

        setEmotion(randomEmotion);
        setTimeout(() => {
          setEmotion("normal");
        }, 1800);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [hovered]);

  const handleClick = () => {
     window.location.href = "/chat-bot";
  };

  return (
    <div
      onClick={handleClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="emoji">
        <div className="eyes">
          <div
            className={`eye ${
              emotion === "wink" ? "wink-left" : ""
            }`}
          />
          <div
            className="eye"
          />
        </div>
        <div
          className={`mouth ${
            hovered ? "smile" : emotion === "surprised" ? "wow" : ""
          }`}
        />
      </div>
    </div>
  );
}