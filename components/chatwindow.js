import { FiUser } from "react-icons/fi";
import styles from "@/styles/chatwindow.module.css";
import { LiaAtomSolid } from "react-icons/lia";

export default function ChatWindow({messages}) {
    // messages format: [{message: "message", sender: "sender", timestamp: "timestamp"}]
    return(
        <div className="chat_messages_container" style={{display: "flex", flexDirection: "column", alignItems: "flex-start"}}>
            {messages.map((message) => {
                return(
                    <div className={`${styles.chat_message_wrapper} ${message.sender == "bot" ? styles.chat_message_wrapper_bot : null}`} style={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
                        <div className="chat_message" style={{ display: "flex", flexDirection: "row" }}>
                            <div style={{ height: "48px", width: "48px", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "18pt", flex: "0 0 auto"}}>
                                {message.sender == "user" ? <FiUser /> : <></>} {message.sender == "bot" ? <LiaAtomSolid></LiaAtomSolid> : <></>}
                            </div>
                            <div style={{ minHeight: "48px", display: "flex", alignItems: "center" }}>
                                {message.message}
                            </div>
                        </div>
                    </div>
                )
            }
            )}
        </div>
    )
}