import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Header from './header';

import "../app/globals.css"


export default function Layout({children, fullHeight = false})
{
    return(
        <>
            <Header></Header>
            <Container style={{maxHeight: fullHeight ? "100%" : ""}}>
                <Row style={{maxHeight: fullHeight ? "100%" : ""}}>
                    {children}
                </Row>
            </Container>
        </>
    )
}