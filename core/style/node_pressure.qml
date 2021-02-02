<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="1" readOnly="0" version="3.4.3-Madeira" styleCategories="LayerConfiguration|Symbology|Labeling">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="RuleRenderer" forceraster="0" enableorderby="0">
    <rules key="{762da8af-38c8-4d28-b881-eec5a63bbbbd}">
      <rule symbol="0" label="&lt;0" filter="&quot;RESULT_PRE&quot; &lt; 0.000000" key="{d2b49035-d790-4300-b1e1-918d26eaa7ed}"/>
      <rule symbol="1" label="0-6" filter="&quot;RESULT_PRE&quot; >= 0.000000 AND &quot;RESULT_PRE&quot; &lt;= 6.000000" key="{911087b0-7f76-4746-8627-2537ed0e4bd6}"/>
      <rule symbol="2" label="6-10" filter="&quot;RESULT_PRE&quot; > 6.000000 AND &quot;RESULT_PRE&quot; &lt;= 10.000000" key="{de4a793b-e142-46bc-b2a7-9429ba1e5784}"/>
      <rule symbol="3" label="10-50" filter="&quot;RESULT_PRE&quot; > 10.000000 AND &quot;RESULT_PRE&quot; &lt;= 50.000000" key="{8d4bf61d-c3dd-4647-8cb3-3a837d8d3b27}"/>
      <rule symbol="4" label=">50" filter="&quot;RESULT_PRE&quot; > 50.000000 AND &quot;RESULT_PRE&quot; &lt;= 1000.000000" key="{1cafc9a6-1771-4fc6-bb1f-cc299bf97516}"/>
      <rule symbol="5" label="NO VALUE" filter="ELSE" key="{d434178d-3e71-4d4e-aff5-e3715996ed36}"/>
    </rules>
    <symbols>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="0" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="215,25,28,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="255,127,0,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="2" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="154,215,244,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="3" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="166,217,106,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="4" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="24,24,228,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="5" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="0,0,0,255" k="color"/>
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style blendMode="0" textOpacity="1" fontItalic="0" fontCapitals="0" fontWordSpacing="0" previewBkgrdColor="#ffffff" useSubstitutions="0" fontUnderline="0" namedStyle="Normal" isExpression="1" fieldName="'Nó '||  &quot;DC_ID&quot;  ||  coalesce('\np='|| format_number(&quot;RESULT_PRE&quot;,1) || '\nH='|| format_number(&quot;RESULT_HEA&quot;,1),'')" textColor="0,0,0,255" fontFamily="MS Shell Dlg 2" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontSizeUnit="Point" fontLetterSpacing="0" fontSize="8.25" multilineHeight="1" fontWeight="50" fontStrikeout="0">
        <text-buffer bufferColor="51,246,20,255" bufferOpacity="1" bufferNoFill="0" bufferJoinStyle="64" bufferBlendMode="0" bufferSizeUnits="MM" bufferDraw="1" bufferSize="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0"/>
        <background shapeRotation="0" shapeFillColor="255,255,255,255" shapeBlendMode="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeDraw="0" shapeSizeY="0" shapeOffsetY="0" shapeSizeType="0" shapeRadiiY="0" shapeSVGFile="" shapeOffsetX="0" shapeRadiiUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeBorderWidthUnit="MM" shapeOpacity="1" shapeRotationType="0" shapeRadiiX="0" shapeOffsetUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="MM" shapeBorderColor="128,128,128,255" shapeBorderWidth="0"/>
        <shadow shadowScale="100" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetUnit="MM" shadowOffsetDist="1" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOpacity="0.7" shadowUnder="0" shadowOffsetGlobal="1" shadowRadius="1.5" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowBlendMode="6" shadowColor="0,0,0,255"/>
        <substitutions/>
      </text-style>
      <text-format rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" multilineAlign="0" decimals="3" autoWrapLength="0" addDirectionSymbol="0" plussign="0" wrapChar="" leftDirectionSymbol="&lt;" formatNumbers="1" placeDirectionSymbol="0" reverseDirectionSymbol="0"/>
      <placement yOffset="0" maxCurvedCharAngleIn="20" priority="5" repeatDistance="0" placement="6" preserveRotation="1" dist="1" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetType="1" maxCurvedCharAngleOut="-20" quadOffset="4" centroidInside="0" repeatDistanceUnits="MM" rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" distUnits="MM" offsetUnits="MapUnit" xOffset="0" distMapUnitScale="3x:0,0,0,0,0,0" placementFlags="10" centroidWhole="0"/>
      <rendering displayAll="0" scaleVisibility="0" zIndex="0" upsidedownLabels="0" scaleMax="10000000" minFeatureSize="0" maxNumLabels="2000" drawLabels="1" fontMaxPixelSize="10000" fontLimitPixelSize="0" labelPerPart="0" obstacleType="0" fontMinPixelSize="3" scaleMin="1" mergeLines="0" obstacle="1" obstacleFactor="1" limitNumLabels="0"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" name="name" value=""/>
          <Option name="properties"/>
          <Option type="QString" name="type" value="collection"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <previewExpression>COALESCE( "RefName", '&lt;NULL>' )</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
