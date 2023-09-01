import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Header from './header';

import "../app/globals.css"


export default function Layout({children})
{
    return(
        <>
            <Header></Header>
            <Container>
                <Row>
                    {children}
                </Row>
            </Container>
        </>
    )
}