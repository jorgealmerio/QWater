<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" minScale="0" simplifyMaxScale="1" readOnly="0" simplifyDrawingHints="0" simplifyDrawingTol="1" simplifyAlgorithm="0" version="3.2.2-Bonn" simplifyLocal="1" labelsEnabled="1" hasScaleBasedVisibilityFlag="0">
  <renderer-v2 forceraster="0" symbollevels="0" type="RuleRenderer" enableorderby="0">
    <rules key="{a63c13fe-8dba-4059-b777-ca94bdb15ff6}">
      <rule label="Com Demanda" symbol="0" filter=" &quot;DEMAND&quot; >0" key="{b19ad7e1-cf31-4cc3-9bb6-f600977a24e0}"/>
      <rule label="Sem Demanda" symbol="1" filter="ELSE" key="{905bac04-a940-4f24-8684-a1cbb6511da6}"/>
    </rules>
    <symbols>
      <symbol alpha="1" name="0" type="marker" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="51,160,44,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" name="1" type="marker" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="227,26,28,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="">
      <rule filter=" &quot;DEMAND&quot; >0" key="">
        <settings>
          <text-style textColor="0,0,0,255" fontWeight="50" fontCapitals="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName="DEMAND" isExpression="0" fontUnderline="0" fontFamily="MS Shell Dlg 2" textOpacity="1" fontSize="8.25" previewBkgrdColor="#ffffff" multilineHeight="1" fontLetterSpacing="0" fontSizeUnit="Point" fontWordSpacing="0" fontStrikeout="0" blendMode="0" namedStyle="Normal" fontItalic="0" useSubstitutions="0">
            <text-buffer bufferDraw="1" bufferColor="51,246,20,255" bufferOpacity="1" bufferBlendMode="0" bufferNoFill="0" bufferJoinStyle="64" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSizeUnits="MM" bufferSize="1"/>
            <background shapeDraw="0" shapeSizeUnit="MM" shapeType="0" shapeFillColor="255,255,255,255" shapeBorderWidth="0" shapeBorderWidthUnit="MM" shapeBorderColor="128,128,128,255" shapeRadiiUnit="MM" shapeRotationType="0" shapeOffsetY="0" shapeSizeX="0" shapeRotation="0" shapeRadiiX="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeBlendMode="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeOpacity="1" shapeSVGFile="" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeRadiiY="0" shapeOffsetX="0" shapeSizeType="0"/>
            <shadow shadowOffsetUnit="MM" shadowOpacity="0.7" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowColor="0,0,0,255" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowBlendMode="6" shadowDraw="0" shadowRadiusUnit="MM" shadowOffsetAngle="135" shadowRadius="1.5" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowUnder="0" shadowScale="100"/>
            <substitutions/>
          </text-style>
          <text-format plussign="0" addDirectionSymbol="0" formatNumbers="1" multilineAlign="0" rightDirectionSymbol=">" leftDirectionSymbol="&lt;" decimals="3" wrapChar="" placeDirectionSymbol="0" reverseDirectionSymbol="0"/>
          <placement fitInPolygonOnly="0" dist="1" placement="6" priority="5" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" yOffset="0" centroidWhole="0" repeatDistance="0" centroidInside="0" maxCurvedCharAngleIn="20" maxCurvedCharAngleOut="-20" rotationAngle="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MapUnit" repeatDistanceUnits="MM" offsetType="1" placementFlags="10" xOffset="0" preserveRotation="1" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" quadOffset="4" distMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM"/>
          <rendering labelPerPart="0" zIndex="0" upsidedownLabels="0" scaleVisibility="0" maxNumLabels="2000" obstacle="1" obstacleType="0" limitNumLabels="0" drawLabels="1" obstacleFactor="1" fontMaxPixelSize="10000" minFeatureSize="0" fontMinPixelSize="3" displayAll="0" fontLimitPixelSize="0" scaleMin="1" scaleMax="10000000" mergeLines="0"/>
          <dd_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </dd_properties>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory width="15" penAlpha="255" opacity="1" rotationOffset="270" scaleDependency="Area" sizeScale="3x:0,0,0,0,0,0" lineSizeScale="3x:0,0,0,0,0,0" penColor="#000000" diagramOrientation="Up" scaleBasedVisibility="0" backgroundAlpha="255" minScaleDenominator="0" penWidth="0" height="15" maxScaleDenominator="1e+8" enabled="0" barWidth="5" sizeType="MM" lineSizeType="MM" labelPlacementMethod="XHeight" backgroundColor="#ffffff" minimumSize="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" zIndex="0" obstacle="0" placement="0" linePlacementFlags="2" priority="0" dist="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties" type="Map">
          <Option name="show" type="Map">
            <Option value="true" name="active" type="bool"/>
            <Option value="DC_ID" name="field" type="QString"/>
            <Option value="2" name="type" type="int"/>
          </Option>
        </Option>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="DC_ID">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" name="IsMultiline" type="QString"/>
            <Option value="0" name="UseHtml" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="ELEVATION">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" name="IsMultiline" type="QString"/>
            <Option value="0" name="UseHtml" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="DEMAND">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" name="IsMultiline" type="QString"/>
            <Option value="0" name="UseHtml" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="PATTERN">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" name="IsMultiline" type="QString"/>
            <Option value="0" name="UseHtml" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="DEMAND_PTO">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" name="IsMultiline" type="QString"/>
            <Option value="0" name="UseHtml" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_DEM">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_HEA">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_PRE">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_QUA">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="DC_ID"/>
    <alias index="1" name="" field="ELEVATION"/>
    <alias index="2" name="" field="DEMAND"/>
    <alias index="3" name="" field="PATTERN"/>
    <alias index="4" name="" field="DEMAND_PTO"/>
    <alias index="5" name="" field="RESULT_DEM"/>
    <alias index="6" name="" field="RESULT_HEA"/>
    <alias index="7" name="" field="RESULT_PRE"/>
    <alias index="8" name="" field="RESULT_QUA"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="DC_ID" expression=""/>
    <default applyOnUpdate="0" field="ELEVATION" expression=""/>
    <default applyOnUpdate="0" field="DEMAND" expression=""/>
    <default applyOnUpdate="0" field="PATTERN" expression=""/>
    <default applyOnUpdate="0" field="DEMAND_PTO" expression=""/>
    <default applyOnUpdate="0" field="RESULT_DEM" expression=""/>
    <default applyOnUpdate="0" field="RESULT_HEA" expression=""/>
    <default applyOnUpdate="0" field="RESULT_PRE" expression=""/>
    <default applyOnUpdate="0" field="RESULT_QUA" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" field="DC_ID" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="ELEVATION" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="DEMAND" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="PATTERN" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="DEMAND_PTO" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="RESULT_DEM" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="RESULT_HEA" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="RESULT_PRE" exp_strength="0" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="RESULT_QUA" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="DC_ID"/>
    <constraint desc="" exp="" field="ELEVATION"/>
    <constraint desc="" exp="" field="DEMAND"/>
    <constraint desc="" exp="" field="PATTERN"/>
    <constraint desc="" exp="" field="DEMAND_PTO"/>
    <constraint desc="" exp="" field="RESULT_DEM"/>
    <constraint desc="" exp="" field="RESULT_HEA"/>
    <constraint desc="" exp="" field="RESULT_PRE"/>
    <constraint desc="" exp="" field="RESULT_QUA"/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="&quot;RESULT_PRE&quot;">
    <columns>
      <column width="-1" name="DC_ID" type="field" hidden="0"/>
      <column width="-1" name="ELEVATION" type="field" hidden="0"/>
      <column width="135" name="DEMAND" type="field" hidden="0"/>
      <column width="-1" name="PATTERN" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
      <column width="-1" name="DEMAND_PTO" type="field" hidden="0"/>
      <column width="-1" name="RESULT_DEM" type="field" hidden="0"/>
      <column width="-1" name="RESULT_HEA" type="field" hidden="0"/>
      <column width="-1" name="RESULT_PRE" type="field" hidden="0"/>
      <column width="-1" name="RESULT_QUA" type="field" hidden="0"/>
    </columns>
  </attributetableconfig>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>C:/Users/Ana/Documents/Almerio/Qgis/plugins/jorgealmerio/Documents/Hydros/Qgis/plugins/QWater/01Alternativas</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- codificação: utf-8 -*-
"""
Os formulários do QGIS podem ter uma função Python que é chamada quando
o formulário
 é aberto.

QGIS forms can have a Python function that is called when the form is
opened.

Use esta função para adicionar lógica extra aos seus formulários.

Entre com o nome da função no campo "Python Init function".
Un exemplo a seguir:
"""
a partir de PyQt4.QtGui importe QWidget

def my_form_open(diálogo, camada, feição):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="DC_ID" editable="1"/>
    <field name="DEMAND" editable="1"/>
    <field name="DEMAND_PTO" editable="1"/>
    <field name="ELEVATION" editable="1"/>
    <field name="PATTERN" editable="1"/>
    <field name="RESULT_DEM" editable="1"/>
    <field name="RESULT_HEA" editable="1"/>
    <field name="RESULT_PRE" editable="1"/>
    <field name="RESULT_QUA" editable="1"/>
    <field name="SAA_Rede_r5_DC_ID" editable="0"/>
    <field name="id" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="DC_ID" labelOnTop="0"/>
    <field name="DEMAND" labelOnTop="0"/>
    <field name="DEMAND_PTO" labelOnTop="0"/>
    <field name="ELEVATION" labelOnTop="0"/>
    <field name="PATTERN" labelOnTop="0"/>
    <field name="RESULT_DEM" labelOnTop="0"/>
    <field name="RESULT_HEA" labelOnTop="0"/>
    <field name="RESULT_PRE" labelOnTop="0"/>
    <field name="RESULT_QUA" labelOnTop="0"/>
    <field name="SAA_Rede_r5_DC_ID" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
  </labelOnTop>
  <widgets>
    <widget name="S01b_AltoGirassol_rede_LENGTH">
      <config/>
    </widget>
  </widgets>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>COALESCE( "RefName", '&lt;NULL>' )</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
