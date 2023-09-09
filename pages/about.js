import Layout from "@/components/layout"
import { Container } from "react-bootstrap"
import Image from 'next/image'

export default function About() {
    return(
        <Layout>
            <Container>
                <div style={{height: "20px"}}></div>
                <h1>About</h1>
                <p>StratoEye is a simple web-interface built to emulate the Air Traffic Radar Tracking Systems, based on Next.js and React.js. StratoEye can be easily extended through WebSockets to interface with trajectory generation and language processing modules.</p>
                <p>StratoEye is fast, lightweight and accessible from all major browsers.</p>
                <h1>Where this was made</h1>
                <div style={{height: "20px"}}></div>
                <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
                    <Image src='/cats.jpg' alt="Building Y cats" width={400} height={300} style={{borderRadius: 10}} />
                    <p>Near a garage where the wild cats live.</p>
                </div>
                
                <h1>Modules</h1>
                <div style={{display: "flex", flexDirection: "row"}}>
                    <div style={{flex: "1 1 0px", display: "flex", justifyContent: "flex-start", alignItems: "center", flexDirection: "column"}}>
                        <Image src="/chatatc.png" alt="StratoEye" width={0} height={0} sizes="100vw" style={{width: "auto", height: "148px"}} />
                        <div>Indigenous StratoEye Simulation Backend.</div>
                    </div>
                    <div style={{flex: "1 1 0px", display: "flex", justifyContent: "flex-start", alignItems: "center", flexDirection: "column"}}>
                        <Image src="/montellama_codex.png" alt="Montellama Codex" width={0} height={0} sizes="100vw" style={{width: "auto", height: "148px"}} />
                        <div style={{textAlign: "center"}}>Montellama Codex version 5 September 2023. Montellama Codex is an instruction fine-tuned Large Language Model based on LLaMA 2 by <a href="https://ai.meta.com">Meta AI</a>.</div>
                    </div>
                </div>
                
                <div style={{height: "20px"}}></div>
            </Container>
        </Layout>
    )
}