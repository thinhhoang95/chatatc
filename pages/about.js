import Layout from "@/components/layout"
import { Container } from "react-bootstrap"
import Image from 'next/image'

export default function About() {
    return(
        <Layout>
            <Container>
                <div style={{height: "20px"}}></div>
                <h1>About</h1>
                <p>ChatATC is a simple web-interface built to emulate the Air Traffic Radar Tracking Systems, based on Next.js and React.js. ChatATC can be easily extended through WebSockets to interface with trajectory generation and language processing modules.</p>
                <p>ChatATC is fast, lightweight and accessible from all major browsers.</p>
                <h1>Where this was made</h1>
                <div style={{height: "20px"}}></div>
                <div style={{display: "flex", "flexDirection": "column", "alignItems": "center"}}>
                    <Image src='/cats.jpg' alt="Building Y cats" width={400} height={300} style={{borderRadius: 10}} />
                    <p>Near a garage where the wild cats live.</p>
                </div>
                
                <h1>Modules</h1>
                <p><strong>Trajectory Generation Module (TRAJEN): </strong> Native ChatATC First-Order Implementation.</p>
                <p><strong>Language Processing Module (LPM): </strong> Montellama CODE version 31 August 2023. Montellama CODE is an instruction fine-tuned Large Language Model based on LLaMA 2 by Meta AI.</p>
                <div style={{height: "20px"}}></div>
            </Container>
        </Layout>
    )
}