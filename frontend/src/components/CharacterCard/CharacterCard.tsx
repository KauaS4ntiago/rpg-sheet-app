import './characterCard.css'
import { Link } from 'react-router-dom'
import Trash from '../../assets/trash.svg'

type Props = {
    name: string
    image: string
    id: number
    onDelete: () => void
}

function CharacterCard({ name, image, id, onDelete }: Props) {

    async function deleteHandleCharacter() {
        if (!window.confirm('Deseja excluir este personagem?')) {
            return
        }

        try {
            const response = await fetch(`/characters/${id}`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            })

            const data = await response.json()

            if (!response.ok) {
                alert(data.error)
                return
            }
            onDelete()

        } catch (error) {
            console.error(error)
            alert('Erro ao conectar ao servidor.')
        }
    }

    return (
        <div className="CharacterCard-container-all">
            <button onClick={deleteHandleCharacter}>
                <img src={Trash} alt="Deletar personagem" />
            </button>

            <div className="CharacterCard-container">
                <Link to={`/character/${id}`}>
                    <img src={image} alt="Imagem de personagem" />
                    <h2>{name}</h2>
                </Link>
            </div>
        </div>
    )
}

export default CharacterCard