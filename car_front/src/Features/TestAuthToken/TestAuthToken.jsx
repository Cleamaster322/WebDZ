import { useState, useEffect } from 'react'

import axios from 'axios'
import api from '../../shared/api.jsx'

function TestAuth() {
  async function getData() {
    console.log(await api.get('/cars/test2/'))
  }

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