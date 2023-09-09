import ChatWindow from '@/components/chatwindow'
import Layout from '@/components/layout'
import { Container, Row, Col, Alert, Button } from 'react-bootstrap'
import Form from 'react-bootstrap/Form'
import InputGroup from 'react-bootstrap/InputGroup'
import { AiOutlineSend } from 'react-icons/ai'
import Image from 'next/image'
import { BsCheckLg } from 'react-icons/bs'
import { GrClose } from 'react-icons/gr'
import { AiOutlineClose } from 'react-icons/ai'

import { useState, useEffect } from 'react'
import PlaneMapper from '@/components/planemapper'

const mqtt = require('mqtt')

export default function ChatNow() {
    const [showJobAlert, setShowJobAlert] = useState(true)
    const [connectStatus, setConnectStatus] = useState('Disconnected')
    const [chatMessages, setChatMessages] = useState([])
    const [chat, setChat] = useState('')

    // MQTT Client Initialization
    const [client, setClient] = useState(null)
    const [planes, setPlanes] = useState([])

    const mqttConnect = (host, mqttOption) => {
        console.log('Now connecting to ', host)
        setConnectStatus('Connecting')
        console.log(mqtt)
        setClient(mqtt.connect(host, mqttOption))
    }

    useEffect(() => {
        if (client) {
            console.log(client)
            client.on('connect', () => {
                setConnectStatus('Connected')
                mqttSub({ topic: 'chatatc-indie/fabrics', qos: 0 })
                mqttSub({ topic: 'chatatc-indie/fabrics-control', qos: 0 })
                console.log('Topics subscribed')
            })
            client.on('error', (err) => {
                console.error('Connection error: ', err)
                client.end()
            })
            client.on('reconnect', () => {
                setConnectStatus('Reconnecting')
            })
            client.on('message', (topic, message) => {
                // const payload = { topic, message: message.toString() };
                // setPayload(payload);
                if (topic == 'chatatc-indie/fabrics') {
                    let messsage = message.toString()
                    // try to parse message to json
                    try {
                        let data = JSON.parse(messsage)
                        console.log(data)
                        if (data.hasOwnProperty('planes')) {
                            setPlanes(data.planes)
                        }
                    } catch (error) {
                        // do nothing
                        console.log('Error parsing JSON!')
                    }
                }

                if (topic == "chatatc-indie/fabrics-control") {
                    let messsage = message.toString()
                    setChatMessages((chatMessages) => {
                        return [
                            ...chatMessages,
                            { message: messsage, sender: 'bot' },
                        ]
                    })
                }
            })
        }
    }, [client])

    const mqttSub = (subscription) => {
        if (client) {
            const { topic, qos } = subscription
            client.subscribe(topic, { qos }, (error) => {
                if (error) {
                    console.log('Subscribe to topics error', error)
                    return
                }
                // setIsSub(true)
            })
        }
    }

    const mqttPublish = (context) => {
        if (client) {
            const { topic, qos, payload } = context
            client.publish(topic, payload, { qos }, (error) => {
                if (error) {
                    console.log('Publish error: ', error)
                }
            })
        }
    }

    const mqttDisconnect = () => {
        if (client) {
            client.end(() => {
                setConnectStatus('Connect')
            })
        }
        setClient(null)
        setPlanes([])
    }

    const connectMQTTButtonHandler = () => {
        const host = 'ws://broker.emqx.io:8083/mqtt'
        const mqttOption = {
            clientId: 'mqttjs_' + Math.random().toString(16).substr(2, 8),
            protocolVersion: 5,
            clean: true,
            reconnectPeriod: 10000,
            connectTimeout: 30 * 1000,
            rejectUnauthorized: false,
            username: 'StratoEye',
        }

        mqttConnect(host, mqttOption)
        return () => {
            mqttDisconnect()
        }
    }

    const handleChatMessageChange = (e) => {
        console.log('Chat message changed')
        setChat(e.target.value)
    }

    const handleChatEnterKey = (e) => {
        if (e.keyCode == 13) {
            // Add to the chatMessages array
            setChatMessages([
                ...chatMessages,
                { message: e.target.value, sender: 'user' },
            ])
            setChat('')
            // Publish to MQTT
            let message = e.target.value
            let payload = {
                message: message,
                sender: 'user',
            }
            mqttPublish({
                topic: 'chatatc-indie/fabrics-instructions',
                qos: 0,
                payload: JSON.stringify(payload),
            })
        }
    }

    return (
        <Layout fullHeight={true}>
            <Container style={{ height: 'calc(100vh - 58px)' }}>
                <Row style={{ height: '100%' }}>
                    <Col
                        md="9"
                        className="noScrollbar"
                        style={{
                            height: '100%',
                            overflowY: 'scroll',
                            paddingTop: '20px',
                        }}
                    >
                        {showJobAlert && (
                            <Alert
                                variant="primary"
                                style={{
                                    display: 'flex',
                                    flexDirection: 'row',
                                }}
                            >
                                <div
                                    style={{
                                        flex: '1 1 auto',
                                        flexWrap: 'wrap',
                                    }}
                                >
                                    I'm also looking for a job 😊. If you like
                                    this, please checkout my CV and other
                                    projects at{' '}
                                    <a href="https://thinhhoang95.github.io">
                                        thinhhoang95.github.io
                                    </a>
                                    .
                                </div>
                                <div
                                    style={{
                                        flex: '0 0 auto',
                                        cursor: 'pointer',
                                    }}
                                >
                                    <GrClose
                                        onClick={() => setShowJobAlert(false)}
                                    ></GrClose>
                                </div>
                            </Alert>
                        )}
                        <Alert
                            variant={`${
                                connectStatus == 'Connected'
                                    ? 'success'
                                    : 'light'
                            }`}
                        >
                            <div
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                }}
                            >
                                <div style={{ flex: '1' }}>
                                    Fabrics{' '}
                                    {connectStatus == 'Connected' ? (
                                        <span style={{ color: 'green' }}>
                                            <BsCheckLg></BsCheckLg>
                                        </span>
                                    ) : (
                                        <span style={{ color: 'red' }}>
                                            <AiOutlineClose></AiOutlineClose>
                                        </span>
                                    )}
                                </div>
                                <div style={{ flex: '1' }}>
                                    Montellama Codex{' '}
                                    {connectStatus == 'Connected' ? (
                                        <span style={{ color: 'green' }}>
                                            <BsCheckLg></BsCheckLg>
                                        </span>
                                    ) : (
                                        <span style={{ color: 'red' }}>
                                            <AiOutlineClose></AiOutlineClose>
                                        </span>
                                    )}{' '}
                                </div>
                                <div style={{ flex: '1' }}>
                                    Indigenous Simulator{' '}
                                    {connectStatus == 'Connected' ? (
                                        <span style={{ color: 'green' }}>
                                            <BsCheckLg></BsCheckLg>
                                        </span>
                                    ) : (
                                        <span style={{ color: 'red' }}>
                                            <AiOutlineClose></AiOutlineClose>
                                        </span>
                                    )}
                                </div>
                                <div style={{ flex: '0 0 auto' }}>
                                    {connectStatus == 'Connected' && (
                                        <Button
                                            onClick={() => mqttDisconnect()}
                                            variant="danger"
                                        >
                                            Disconnect
                                        </Button>
                                    )}
                                    {connectStatus !== 'Connected' && (
                                        <Button
                                            onClick={() =>
                                                connectMQTTButtonHandler()
                                            }
                                            variant="success"
                                        >
                                            Connect
                                        </Button>
                                    )}
                                </div>
                            </div>
                            <div></div>
                        </Alert>
                        <div
                            style={{
                                display: 'flex',
                                justifyContent: 'center',
                            }}
                        >
                            {/* <Image src="/vvts.png" alt="Shortest Path" width={0} height={0} sizes="100vw" style={{ width: '500px', height: '500px' }}/> */}
                            <PlaneMapper planes={planes}></PlaneMapper>
                        </div>
                        <div
                            style={{
                                display: 'flex',
                                justifyContent: 'center',
                                marginTop: 12,
                                fontStyle: 'italic',
                            }}
                        >
                            StratoEye & Montellama Codex might be unreliable.
                        </div>
                    </Col>
                    <Col
                        md="3"
                        style={{ paddingTop: '20px' }}
                    >
                        <div
                            style={{
                                display: 'flex',
                                flexDirection: 'column',
                                height: '100%',
                            }}
                        >
                            <div style={{ flex: '0' }}>
                                <ChatWindow
                                    messages={chatMessages}
                                ></ChatWindow>
                            </div>
                            <div style={{ flex: '1' }}></div>
                            <div style={{ flex: '0' }}>
                                <InputGroup className="mb-3">
                                    <InputGroup.Text id="basic-addon1">
                                        <AiOutlineSend></AiOutlineSend>
                                    </InputGroup.Text>
                                    <Form.Control
                                        placeholder="Message"
                                        aria-label="Message"
                                        aria-describedby="basic-addon1"
                                        onChange={(e) =>
                                            handleChatMessageChange(e)
                                        }
                                        onKeyDown={(e) => handleChatEnterKey(e)}
                                        value={chat}
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
