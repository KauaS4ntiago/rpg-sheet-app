import NavBar from '../../components/NavBar/NavBar';
import Plus from '../../assets/plus.svg'
import CharacterCard from '../../components/CharacterCard/CharacterCard';
import './dashBoard.css'
import { useEffect, useState } from 'react';

function DashBoard() {
    interface Character {
        id: number
        name: string
        image: string
    }

    const [search, setSearch] = useState('')
    const [characters, setCharacters] = useState<Character[]>([])

    const loadCharacters = () => {
    const userId = localStorage.getItem('user_id')

    fetch(`/characters/user/${userId}`, {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then(response => response.json())
    .then(data => { if(data.error) {
            alert(data.error)
        } else {
            setCharacters(data)
        }
    })
}

    const getImageUrl = (path: string) => {
        if (!path) return '';
        if (path.startsWith('http')) return path; // já é uma URL completa (ex: placehold.co)
    return `/characters/uploads/${path}`;
    };

    useEffect(() => { loadCharacters()},[])
        
    const filteredCharacters = characters.filter(
        character => character.name.toLowerCase().includes(search.toLowerCase())
    )

    function handleCreateCharacter() {
        const data = {
            user_id: localStorage.getItem('user_id'),
            name: 'Personagem novo',
            current_hp: 0,
            max_hp: 0,
            current_sanity: 0,
            max_sanity: 0,
            defense: 0,
            image: 'https://placehold.co/100x100',
            notes: 'Digite suas anotações aqui',
            attributes: [
                { name: 'Intelecto', value: 0 },
                { name: 'Força', value: 0 },
                { name: 'Vigor', value: 0 },
                { name: 'Agilidade', value: 0 },
                { name: 'Presença', value: 0 }
            ],
            skills: [
                { name: 'Perícia 1', value: 0 },
                { name: 'Perícia 2', value: 0 },
                { name: 'Perícia 3', value: 0 },
                { name: 'Perícia 4', value: 0 },
                { name: 'Perícia 5', value: 0 },
                { name: 'Perícia 6', value: 0 },
                { name: 'Perícia 7', value: 0 },
                { name: 'Perícia 8', value: 0 },
                { name: 'Perícia 9', value: 0 },
                { name: 'Perícia 10', value: 0 }
            ],
            abilities: [
                { name: 'Bola de Fogo', description: 'Uma bola de fogo poderosa', image: null }
            ]
        }
        fetch('/characters', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if(data.error) {
                    alert(data.error)
            } else {
                    loadCharacters()
            }})
        }

    return (
        <div className='DashBoard-container'>
           <NavBar search={search} setSearch={setSearch} />
           <div className='DashBoard-content'>
                <div className='DashBoard-header'>
                <h1>Meus personagens</h1>
                <button className='DashBoard-button' onClick={handleCreateCharacter}><img src={Plus} alt="Adicionar"/></button>
                </div>
            <ul className='Dashboard-list'>
                {filteredCharacters.map(character => (
                    <CharacterCard name={character.name} image={getImageUrl(character.image)} id={character.id} key={character.id}/>
                ))}
            </ul>
           </div>
            
        </div>
    )
}

export default DashBoard