import { useEffect, useState } from "react"
import { ActivityIndicator, ScrollView, Text, TouchableOpacity, View } from "react-native"
import API, { endpoints } from "../../configs/API"

const { default: MyStyle } = require("../../styles/MyStyle")




const Home = ({ route }) => {
    const [activities, setActivities] = useState(null)
    const actId = route.params?.actId;

    useEffect(() => {
        const loadActivities = async () => {
            let url = endpoints['activities']

            if (actId !== undefined && actId !== null)
                url = `${url}?q=${actId}`

            try {
                let res = await API.get(url);
                setActivities(res.data.results);
            }
            catch (ex) {
                setActivities([]);
                console.error(ex)
            }
        }
        loadActivities();
    }, [actId])

    return (
        <View style={MyStyle.container}>
            <Text style={MyStyle.name}>Danh sách hoạt động ngoại khóa</Text>
            <ScrollView style={{ flex: 1, }}>
                {activities === null ? <ActivityIndicator /> : <>
                    {activities.map(c => (
                        <View key={c.id}>
                            <TouchableOpacity style={{ flex: 3 }}>
                                <Text>{c.name}</Text>
                            </TouchableOpacity>
                            <Text style={{ fontSize: 50 }}>{c.description}</Text>
                        </View>
                    ))}
                </>}
            </ScrollView>
        </View>
    )
}

export default Home;