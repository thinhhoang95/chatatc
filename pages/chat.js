import ChatWindow from "@/components/chatwindow";
import Layout from "@/components/layout"
import { Container, Row, Col, Alert } from "react-bootstrap"
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import { AiOutlineSend } from 'react-icons/ai';
import Image from 'next/image'
import { BsCheckLg } from 'react-icons/bs';
import { GrClose } from 'react-icons/gr';

import { useState } from "react";

export default function ChatNow() {
    const [showJobAlert, setShowJobAlert] = useState(true);

    return(
        <Layout>
            <Container style={{height: "calc(100vh - 130px)"}}>
                <div style={{height: "20px"}}></div>
                <Row style={{height: "100%"}}>
                    <Col md="9">
                        {showJobAlert && <Alert variant="primary" style={{"display": "flex", "flexDirection": "row"}}>
                            <div style={{"flex": "1 1 auto", "flexWrap": "wrap"}}>
                                I'm also looking for a job. If you like this, please checkout my CV and other projects at <a href="https://thinhhoang95.github.io">thinhhoang95.github.io</a>.
                            </div>
                            <div style={{"flex": "0 0 auto", "cursor": "pointer"}}>
                                <GrClose onClick={() => setShowJobAlert(false)}></GrClose>
                            </div>
                        </Alert>}
                        <Alert variant="light">
                            <div style={{display: "flex"}}>
                                <div style={{flex: "1"}}>MQTT Server <span style={{color: 'green'}}><BsCheckLg></BsCheckLg></span></div>
                                <div style={{flex: "1"}}>Montellama Codex <span style={{color: 'green'}}><BsCheckLg></BsCheckLg></span></div>
                                <div style={{flex: "1"}}>Trajen Simulator <span style={{color: 'green'}}><BsCheckLg></BsCheckLg></span></div>
                            </div>
                        </Alert>

                        <Image src="/shortestcrop.gif" alt="Shortest Path" width={0} height={0} sizes="100vw" style={{ width: '100%', height: 'auto' }}/>
                        <div style={{display: 'flex', justifyContent: 'center', marginTop: 12}}>
                            ChatATC & Montellama Codex might be unreliable.
                        </div>
                    </Col>
                    <Col md="3">
                        <div style={{display: "flex", flexDirection: "column", height: "100%"}}>
                            <div style={{flex: "0"}}>
                                <ChatWindow messages={[{message: "envoy 288, turn right heading 120", sender: "user", timestamp: "timestamp"},{message: "hdg('envoy 288', 120)", sender: "bot", timestamp: "timestamp"}]}></ChatWindow>
                            </div>
                            <div style={{flex: "1"}}></div>
                            <div style={{flex: "0"}}>
                                <InputGroup className="mb-3">
                                    <InputGroup.Text id="basic-addon1"><AiOutlineSend></AiOutlineSend></InputGroup.Text>
                                    <Form.Control
                                    placeholder="Message"
                                    aria-label="Message"
                                    aria-describedby="basic-addon1"
                                    />
                                </InputGroup>
                            </div>
                        </div>
                    </Col>
                </Row>
            </Container>
        </Layout>
    )
}