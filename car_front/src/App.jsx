import { useState} from 'react'
import './App.css'
import Test from './Features/Test/Test.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
   <>
       <Test/>
       <Test/>
       <Test/>
   </>
  )
}

export default App
