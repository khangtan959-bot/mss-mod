package com.coreblockstudios.mss.item;

import com.coreblockstudios.mss.MSS;
import com.coreblockstudios.mss.entity.MSSEntities;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.BookItem;
import net.minecraft.world.item.SpawnEggItem;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public class MSSItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MSS.MODID);

    public static final DeferredItem<Item> INFO_BOOK = ITEMS.register("info_book",
            () -> new BookItem(new Item.Properties().stacksTo(1)));

    public static final DeferredItem<SpawnEggItem> MUMMY_SPAWN_EGG = ITEMS.register("mummy_spawn_egg",
            () -> new SpawnEggItem(MSSEntities.MUMMY.get(), 0x8B7355, 0xD4B896, new Item.Properties()));

    public static final DeferredItem<SpawnEggItem> SPIRIT_SPAWN_EGG = ITEMS.register("spirit_spawn_egg",
            () -> new SpawnEggItem(MSSEntities.SPIRIT.get(), 0xE8E4D4, 0x9EB0B8, new Item.Properties()));

    public static final DeferredItem<SpawnEggItem> QUEEN_SPIDER_SPAWN_EGG = ITEMS.register("queen_spider_spawn_egg",
            () -> new SpawnEggItem(MSSEntities.QUEEN_SPIDER.get(), 0x2B1F1F, 0x8B0000, new Item.Properties()));

    public static void register(net.neoforged.bus.api.IEventBus bus) {
        ITEMS.register(bus);
    }
}
