  import { SOLNLIMIT, SOLNINITIALOFFSET } from './config.js';

  export const getSolutionData = async ( url = '/', q = {})=>{
    
      const response = await fetch(`${url}?limit=${q['limit']}&offset=${q['offset']}&category=${q['category']}`, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
      },
    });
  
      try {
        const solnData = await response.json();
               return solnData
      }catch(error) {
        console.log("error", error);
      }
  }

