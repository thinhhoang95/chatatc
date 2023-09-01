import Layout from "@/components/layout"
import { Container } from "react-bootstrap"
import Image from 'next/image'

export default function About() {
    return(
        <Layout>
            <Container>
                <div style={{height: "60px"}}></div>
                <h1>About</h1>
                <p>ChatATC is a simple web-interface built to emulate the Air Traffic Radar Tracking Systems, based on Next.js and React.js. ChatATC can be easily extended through WebSockets to interface with trajectory generation and language processing modules.</p>
                <p>ChatATC is fast, lightweight and accessible from all major browsers.</p>
                <h1>Origin</h1>
                <p>Near a garage where the wild cats live.</p>
                <h1>Modules</h1>
                <p><strong>Trajectory Generation Module (TRAJEN): </strong> Native ChatATC First-Order Implementation.</p>
                <p><strong>Language Processing Module (LPM): </strong> Montellama CODE version 31 August 2023.</p>
                <div style={{display: 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'flexDirection': 'column'}}>
                    <div style={{height: "20px"}}></div>
                    <Image src='/montellama.png' alt="Montellama Code Mascot" width={200} height={200} />
                    <div>Montellama Mascot (Thinh x DALL-E)</div>
                </div>
                <div style={{height: "60px"}}></div>
            </Container>
        </Layout>
    )
}