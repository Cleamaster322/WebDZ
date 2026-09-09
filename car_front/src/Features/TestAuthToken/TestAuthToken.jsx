import {useEffect} from 'react'

import api from '../../shared/api.jsx'

function TestAuth() {
    useEffect(() => {
        api.get('/cars/test2/')
    }, [])

    return (
        <>
            <div></div>
        </>
    )
}

export default TestAuth