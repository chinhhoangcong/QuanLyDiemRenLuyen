import { Text, View } from "react-native"

const { default: MyStyle } = require("../../styles/MyStyle")




const Home = () => {
    return (
        <View style={MyStyle.container}>
            <Text>Home</Text>
        </View>
    )
}

export default Home