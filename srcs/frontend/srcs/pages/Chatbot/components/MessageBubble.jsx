import styles from './MessageBubble.module.css';

export default function MessageBubble({ message }) {
  return (
    <div className={`${styles.bubbleWrapper} ${styles[message.sender]}`}>
      <div className={styles.bubble}>
        {message.text}
      </div>
    </div>
  );
}
